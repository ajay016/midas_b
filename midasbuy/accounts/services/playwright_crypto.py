"""
Makes Midasbuy API calls from inside a live browser session.

WHY headed mode (headless=False):
  The Tencent Chaos VM reads Forter's blackbox-selection from sessionStorage
  and WebGL/canvas data at encryption time.  In headless Playwright these are
  absent or blank — the Forter SDK detects headless mode and never writes
  blackbox-selection → Chaos VM produces only ~216-char encrypt_msg (missing
  ~900 bytes of fingerprint) → server returns HTTP 500.

  With headless=False the browser has a real GPU-backed rendering pipeline.
  Forter generates a proper blackbox, Chaos VM produces ~1456-char encrypt_msg,
  and the server accepts it.  --start-minimized keeps the window off-screen.
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# ── Stealth init script ───────────────────────────────────────────────────────
# Applied to every new context to prevent bot-detection by the Forter SDK.
_STEALTH_JS = """
(() => {
    // webdriver
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

    // window.chrome — its absence is the #1 headless tell
    if (!window.chrome) {
        Object.defineProperty(window, 'chrome', {
            writable: true, enumerable: true, configurable: false,
            value: {
                app: {
                    isInstalled: false,
                    InstallState: { DISABLED:'disabled', INSTALLED:'installed', NOT_INSTALLED:'not_installed' },
                    RunningState: { CANNOT_RUN:'cannot_run', READY_TO_RUN:'ready_to_run', RUNNING:'running' },
                    getDetails: function(){}, getIsInstalled: function(){ return false; },
                    installState: function(){}, runningState: function(){ return 'cannot_run'; },
                },
                csi: function(){},
                loadTimes: function(){ return {}; },
                runtime: {},
            },
        });
    }

    // plugins — empty array is a headless tell
    try {
        if (!navigator.plugins || navigator.plugins.length === 0) {
            const mk = (n, f) => ({ name: n, filename: f, description: 'Portable Document Format',
                length: 1, 0: { type: 'application/pdf', suffixes: 'pdf', description: '' } });
            const list = [
                mk('PDF Viewer', 'internal-pdf-viewer'),
                mk('Chrome PDF Viewer', 'internal-pdf-viewer'),
                mk('Chromium PDF Viewer', 'internal-pdf-viewer'),
            ];
            Object.defineProperty(navigator, 'plugins', { get: () => list, enumerable: true });
        }
    } catch(e) {}

    // languages / platform / concurrency
    try { Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); } catch(e) {}
    try { Object.defineProperty(navigator, 'platform',  { get: () => 'Win32' }); } catch(e) {}
    try {
        if (!navigator.hardwareConcurrency || navigator.hardwareConcurrency < 2)
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    } catch(e) {}

    // Permissions API — headless has different behaviour
    try {
        const origQuery = window.Permissions && window.Permissions.prototype.query;
        if (origQuery) {
            window.Permissions.prototype.query = function(p) {
                if (p && p.name === 'notifications')
                    return Promise.resolve({ state: Notification.permission });
                return origQuery.call(this, p);
            };
        }
    } catch(e) {}
})();
"""

# ── JS snippets evaluated inside the page ────────────────────────────────────

_JS_CALL_API = """
async ({payloadJson, endpoint, method}) => {
    try {
        const tokenEl = document.getElementById('xMidasToken');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const versionEl  = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0)
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));
        const enc_len     = encrypt_msg.length;

        const resp = await fetch('https://www.midasbuy.com' + endpoint, {
            method:      method || 'POST',
            headers:     { 'Content-Type': 'application/json', 'Accept': 'application/json, text/plain, */*' },
            body:        JSON.stringify({encrypt_msg, ctoken_ver, ctoken}),
            credentials: 'include',
        });

        const text = await resp.text();
        let data;
        try { data = JSON.parse(text); }
        catch(e) {
            const hdrs = {};
            for (const [k, v] of resp.headers.entries()) hdrs[k] = v;
            return {error: 'invalid_json', status: resp.status,
                    encrypt_msg_len: enc_len,
                    text: text.substring(0, 300),
                    response_headers: hdrs};
        }
        return {ok: true, status: resp.status, data, encrypt_msg_len: enc_len};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""

_JS_ENCRYPT_ONLY = """
({payloadJson}) => {
    try {
        const tokenEl   = document.getElementById('xMidasToken');
        const versionEl = document.getElementById('xMidasVersion');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0)
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));
        return {ok: true, ctoken, ctoken_ver, encrypt_msg};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_session_storage(storage_state_path: str) -> dict:
    ss_path = os.path.join(os.path.dirname(storage_state_path), "session_storage.json")
    if not os.path.exists(ss_path):
        return {}
    try:
        with open(ss_path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("[CRYPTO] loaded %d sessionStorage keys", len(data))
        return data
    except Exception as e:
        logger.warning("[CRYPTO] could not load session_storage.json: %s", e)
        return {}


def _load_manual_blackbox(storage_state_path: str) -> str:
    """
    Load a manually saved Forter blackbox-selection value.

    The Forter SDK refuses to generate this in any Playwright context (headless
    or headed) because it uses timing-based CDP detection.  The only reliable
    fix is to capture the value from a real Chrome session and save it here.

    How to get the value:
      1. Open https://www.midasbuy.com/midasbuy/bd/redeem/pubgm in Chrome
      2. DevTools → Application → Session Storage → https://www.midasbuy.com
      3. Find the 'blackbox-selection' row, copy the value
      4. Save it to: <session_dir>/blackbox_selection.txt

    The value is device-specific and stays valid for days to weeks.
    """
    path = os.path.join(os.path.dirname(storage_state_path), "blackbox_selection.txt")
    if not os.path.exists(path):
        logger.warning(
            "[CRYPTO] blackbox_selection.txt not found at %s — "
            "encrypt_msg will be small and the server will return 500.  "
            "See the docstring above for how to create this file.", path
        )
        return ""
    try:
        value = open(path, encoding="utf-8").read().strip()
        if value:
            logger.info("[CRYPTO] loaded manual blackbox-selection  len=%d", len(value))
            return value
        logger.warning("[CRYPTO] blackbox_selection.txt is empty")
    except Exception as e:
        logger.warning("[CRYPTO] could not read blackbox_selection.txt: %s", e)
    return ""


def _launch_context(p, storage_state_path: str):
    """
    Launch a headed browser (headless=False) so the Forter SDK gets real
    GPU/canvas/WebGL data and generates a valid blackbox-selection.
    --start-minimized keeps the window invisible on Windows.
    """
    ss_data = _load_session_storage(storage_state_path)

    browser = p.chromium.launch(
        headless=False,           # MUST be False — headless blocks Forter SDK
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--start-minimized",  # Window opens minimized (off-screen on Windows)
            "--window-size=1440,900",
            "--disable-infobars",
        ],
    )

    context = browser.new_context(
        storage_state=storage_state_path,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/New_York",
        # No user_agent override: let Playwright use the natural UA so it matches
        # the auto-generated sec-ch-ua header (mismatch is a bot signal).
    )

    # Stealth patches — prevent headless detection by Forter SDK
    context.add_init_script(_STEALTH_JS)

    # Pre-load any previously saved sessionStorage (best-effort)
    if ss_data:
        ss_json = json.dumps(ss_data)
        context.add_init_script(f"""
            (() => {{
                const data = {ss_json};
                for (const [k, v] of Object.entries(data)) {{
                    try {{ sessionStorage.setItem(k, v); }} catch(e) {{}}
                }}
            }})();
        """)
        logger.info("[CRYPTO] pre-injecting %d sessionStorage keys", len(ss_data))

    # Inject manually saved Forter blackbox — overrides any auto-generated (empty) value.
    # This is the primary fix: Forter's CDP-timing detection blocks automatic generation
    # in every Playwright context, so we supply a real browser's value here.
    manual_blackbox = _load_manual_blackbox(storage_state_path)
    if manual_blackbox:
        context.add_init_script(f"""
            (() => {{
                try {{ sessionStorage.setItem('blackbox-selection', {json.dumps(manual_blackbox)}); }}
                catch(e) {{}}
            }})();
        """)
        logger.info("[CRYPTO] injected manual blackbox-selection")

    return browser, context


def _wait_for_xmidas(page, session_dir: str, timeout_ms: int) -> bool:
    from playwright.sync_api import TimeoutError as PWTimeout

    try:
        page.wait_for_function(
            "() => !!document.getElementById('xMidasToken')?.value",
            timeout=timeout_ms,
        )
        logger.info("[CRYPTO] xMidasToken ready")
    except PWTimeout:
        logger.error("[CRYPTO] timeout waiting for xMidasToken")
        _save_debug(page, session_dir, "crypto_no_token")
        return False

    try:
        page.wait_for_function(
            "() => typeof window.xMidas === 'function'",
            timeout=15_000,
        )
        logger.info("[CRYPTO] window.xMidas ready")
    except PWTimeout:
        logger.warning("[CRYPTO] window.xMidas not ready — trying anyway")

    # Log whether the injected blackbox is present
    try:
        blen = page.evaluate(
            "() => (window.sessionStorage.getItem('blackbox-selection') || '').length"
        )
        if blen:
            logger.info("[CRYPTO] blackbox-selection present  len=%d", blen)
        else:
            logger.warning(
                "[CRYPTO] blackbox-selection is empty — "
                "create midasbuy_sessions/account_<N>/blackbox_selection.txt "
                "with the value from Chrome DevTools → Application → Session Storage"
            )
    except Exception:
        pass

    return True


# ── Public API ────────────────────────────────────────────────────────────────

def call_api_in_browser(
    payload: dict,
    endpoint: str,
    storage_state_path: str,
    country_code: str = "bd",
    method: str = "POST",
    timeout_ms: int = 60_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page, then execute window.xMidas AND
    fetch() entirely inside the browser tab.

    Returns the parsed JSON response dict, or None on failure.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("[CRYPTO] Playwright not installed")
        return None

    redeem_url  = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser, context = _launch_context(p, storage_state_path)
            page = context.new_page()

            logger.info("[CRYPTO] navigating to %s", redeem_url)
            try:
                page.goto(redeem_url, wait_until="domcontentloaded", timeout=timeout_ms)
            except PWTimeout:
                logger.error("[CRYPTO] page.goto timed out")
                _save_debug(page, session_dir, "crypto_timeout")
                browser.close()
                return None

            logger.info("[CRYPTO] page loaded  url=%s", page.url)

            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling in-browser fetch  endpoint=%s", endpoint)

            result = page.evaluate(_JS_CALL_API, {
                "payloadJson": payload_json,
                "endpoint":    endpoint,
                "method":      method,
            })

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result:
                logger.error("[CRYPTO] evaluate returned None")
                return None

            if result.get("error"):
                logger.error(
                    "[CRYPTO] JS/fetch error  error=%s  status=%s  "
                    "encrypt_msg_len=%s  response_headers=%s  text=%.200s",
                    result.get("error"),
                    result.get("status"),
                    result.get("encrypt_msg_len", "?"),
                    result.get("response_headers", {}),
                    result.get("text", ""),
                )
                return None

            logger.info(
                "[CRYPTO] browser fetch ok  status=%s  encrypt_msg_len=%s",
                result.get("status"),
                result.get("encrypt_msg_len"),
            )
            return result.get("data")

    except Exception:
        logger.exception("[CRYPTO] call_api_in_browser crashed")
        return None


def get_browser_payload(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page, call window.xMidas, and return
    {encrypt_msg, ctoken, ctoken_ver, fresh_cookies}.

    Prefer call_api_in_browser() when you also need to make the HTTP request.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("[CRYPTO] Playwright not installed")
        return None

    redeem_url  = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser, context = _launch_context(p, storage_state_path)
            page = context.new_page()

            logger.info("[CRYPTO] navigating to %s", redeem_url)
            try:
                page.goto(redeem_url, wait_until="domcontentloaded", timeout=timeout_ms)
            except PWTimeout:
                logger.error("[CRYPTO] page.goto timed out")
                _save_debug(page, session_dir, "crypto_timeout")
                browser.close()
                return None

            logger.info("[CRYPTO] page loaded  url=%s", page.url)

            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            result = page.evaluate(_JS_ENCRYPT_ONLY, {"payloadJson": payload_json})

            fresh_cookies = {
                c["name"]: c["value"]
                for c in context.cookies()
                if c.get("name") and c.get("value")
            }

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result or result.get("error"):
                logger.error("[CRYPTO] JS error: %s", result)
                return None

            logger.info(
                "[CRYPTO] ok  ctoken_prefix=%s  encrypt_msg_len=%d",
                result["ctoken"][:20],
                len(result["encrypt_msg"]),
            )
            return {
                "encrypt_msg":   result["encrypt_msg"],
                "ctoken":        result["ctoken"],
                "ctoken_ver":    result["ctoken_ver"],
                "fresh_cookies": fresh_cookies,
            }

    except Exception:
        logger.exception("[CRYPTO] get_browser_payload crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts saved: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)
