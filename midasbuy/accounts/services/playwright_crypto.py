"""
Makes Midasbuy API calls from inside a live browser session.

Root cause of HTTP 500:
  The Tencent Chaos VM reads Forter's device tokens (forterToken, feh--* keys)
  from localStorage when encrypting.  Standard Playwright is detected as a
  bot by Forter via CDP timing analysis, so it never writes those tokens.
  Result: Chaos VM produces only ~216-char encrypt_msg; server rejects it.

Fix: use patchright (drop-in Playwright replacement that removes all CDP
  detection markers).  With patchright, Forter SDK runs normally, writes
  forterToken + feh--* to localStorage during the login session, those values
  are saved in storage_state.json, and every subsequent call produces the
  expected ~1456-char encrypt_msg.

Install once:
  pip install patchright
  patchright install chromium
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def _get_playwright():
    """Prefer patchright (undetected); fall back to standard playwright."""
    try:
        from patchright.sync_api import sync_playwright, TimeoutError as PWTimeout
        logger.debug("[CRYPTO] using patchright")
        return sync_playwright, PWTimeout
    except ImportError:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
        logger.warning(
            "[CRYPTO] patchright not installed — Forter SDK will be blocked by CDP "
            "detection and forterToken won't be written → encrypt_msg will be ~216 chars "
            "→ server will return 500.  Fix: pip install patchright && patchright install chromium"
        )
        return sync_playwright, PWTimeout


# ── Stealth init script (belt-and-suspenders on top of patchright) ────────────
_STEALTH_JS = """
(() => {
    try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch(e) {}

    if (!window.chrome) {
        try {
            Object.defineProperty(window, 'chrome', {
                writable: true, enumerable: true, configurable: false,
                value: {
                    app: { isInstalled: false, getDetails(){}, getIsInstalled(){ return false; },
                           installState(){}, runningState(){ return 'cannot_run'; } },
                    csi(){}, loadTimes(){ return {}; }, runtime: {},
                },
            });
        } catch(e) {}
    }

    try {
        if (!navigator.plugins || navigator.plugins.length === 0) {
            const mk = (n, f) => ({ name: n, filename: f,
                description: 'Portable Document Format', length: 1,
                0: { type: 'application/pdf', suffixes: 'pdf', description: '' } });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [mk('PDF Viewer','internal-pdf-viewer'),
                            mk('Chrome PDF Viewer','internal-pdf-viewer'),
                            mk('Chromium PDF Viewer','internal-pdf-viewer')],
                enumerable: true,
            });
        }
    } catch(e) {}

    try { Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] }); } catch(e) {}
    try { Object.defineProperty(navigator, 'platform',  { get: () => 'Win32' }); } catch(e) {}
    try {
        if (!navigator.hardwareConcurrency || navigator.hardwareConcurrency < 2)
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    } catch(e) {}

    // Capture window.xMidas the instant the Chaos VM assigns it.
    // The SPA may clear window.xMidas during hydration, but our getter still
    // returns the captured reference so page.evaluate() always sees a function.
    try {
        let _xMidasCapture = undefined;
        Object.defineProperty(window, 'xMidas', {
            get:          () => _xMidasCapture,
            set: (fn) => { if (typeof fn === 'function') _xMidasCapture = fn; },
            configurable: true,
            enumerable:   true,
        });
    } catch(e) {}
})();
"""

# ── JS evaluated inside the page ──────────────────────────────────────────────

_JS_CALL_API = """
async ({payloadJson, endpoint, method}) => {
    try {
        // xMidasToken: wait up to 15s for SPA to finish hydrating
        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        const tokenEl = document.getElementById('xMidasToken');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const versionEl  = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        // xMidas: wait up to 15s for the Chaos VM script to finish loading
        let xmWait = 0;
        while (typeof window.xMidas !== 'function' && xmWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            xmWait++;
        }
        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        // Snapshot localStorage Forter data before calling xMidas (for debugging)
        const ftPresent  = !!localStorage.getItem('forterToken');
        const fehCount   = Object.keys(localStorage).filter(k => k.startsWith('feh--')).length;

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
            for (const [k,v] of resp.headers.entries()) hdrs[k] = v;
            return {error: 'invalid_json', status: resp.status,
                    encrypt_msg_len: enc_len,
                    forter_token_present: ftPresent, feh_count: fehCount,
                    response_headers: hdrs, text: text.substring(0, 300)};
        }
        return {ok: true, status: resp.status, data,
                encrypt_msg_len: enc_len,
                forter_token_present: ftPresent, feh_count: fehCount};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack||'').substring(0,500)};
    }
}
"""

_JS_ENCRYPT_ONLY = """
async ({payloadJson}) => {
    try {
        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        const tokenEl   = document.getElementById('xMidasToken');
        const versionEl = document.getElementById('xMidasVersion');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        let xmWait = 0;
        while (typeof window.xMidas !== 'function' && xmWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            xmWait++;
        }
        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0)
            return {error: 'xmidas_empty'};

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));
        return {ok: true, ctoken, ctoken_ver, encrypt_msg};
    } catch(e) {
        return {error: 'js_exception', detail: String(e)};
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


def _log_storage_state_locals(storage_state_path: str) -> None:
    """Log localStorage contents from storage_state to verify Forter data is present."""
    try:
        with open(storage_state_path, encoding="utf-8") as f:
            ss = json.load(f)
        for origin in ss.get("origins", []):
            ls_items = origin.get("localStorage", [])
            if not ls_items:
                continue
            keys = [item["name"] for item in ls_items]
            forter_keys = [k for k in keys if k.startswith("feh--") or k == "forterToken"]
            logger.info(
                "[CRYPTO] storage_state localStorage  origin=%s  total=%d  forter_keys=%s",
                origin.get("origin"), len(ls_items), forter_keys,
            )
        if not any(o.get("localStorage") for o in ss.get("origins", [])):
            logger.warning(
                "[CRYPTO] storage_state has NO localStorage data — "
                "Forter SDK did not run during login. "
                "Install patchright so it writes forterToken during login: "
                "pip install patchright && patchright install chromium"
            )
    except Exception as e:
        logger.debug("[CRYPTO] could not inspect storage_state: %s", e)


def _launch_context(p, storage_state_path: str):
    """Launch headless browser. With patchright, Forter SDK runs undetected."""
    ss_data = _load_session_storage(storage_state_path)
    _log_storage_state_locals(storage_state_path)

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ],
    )

    context = browser.new_context(
        storage_state=storage_state_path,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/New_York",
    )

    context.add_init_script(_STEALTH_JS)

    if ss_data:
        ss_json = json.dumps(ss_data)
        context.add_init_script(f"""
            (() => {{
                const data = {ss_json};
                for (const [k,v] of Object.entries(data)) {{
                    try {{ sessionStorage.setItem(k, v); }} catch(e) {{}}
                }}
            }})();
        """)

    return browser, context


def _wait_for_xmidas(page, session_dir: str, timeout_ms: int) -> bool:
    from playwright.sync_api import TimeoutError as PWTimeout
    try:
        from patchright.sync_api import TimeoutError as PWTimeout
    except ImportError:
        pass

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

    # Log whether Forter wrote its tokens (tells us if patchright is working)
    try:
        info = page.evaluate("""
            () => ({
                forterToken: !!localStorage.getItem('forterToken'),
                fehCount:    Object.keys(localStorage).filter(k => k.startsWith('feh--')).length,
            })
        """)
        if info.get("forterToken"):
            logger.info("[CRYPTO] Forter localStorage ready  feh_count=%d", info.get("fehCount", 0))
        else:
            logger.warning(
                "[CRYPTO] forterToken missing from localStorage  "
                "(patchright not active? run: pip install patchright && patchright install chromium)"
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
    Navigate to the Midasbuy redeem page, run window.xMidas and fetch()
    entirely inside the browser, return the parsed JSON response.
    """
    sync_playwright, PWTimeout = _get_playwright()

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

            # Diagnostic: confirm xMidas state from Python side right before calling
            try:
                diag = page.evaluate("""
                    () => ({
                        xMidasType:    typeof window.xMidas,
                        xMidasToken:   !!document.getElementById('xMidasToken')?.value,
                        url:           location.href,
                        readyState:    document.readyState,
                        midasKeys:     Object.keys(window).filter(k => k.toLowerCase().includes('midas')),
                    })
                """)
                logger.info("[CRYPTO] pre-call diag: %s", diag)
            except Exception as _e:
                logger.warning("[CRYPTO] diag failed: %s", _e)

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
                    "[CRYPTO] fetch failed  error=%s  status=%s  "
                    "encrypt_msg_len=%s  forter_token=%s  feh_count=%s",
                    result.get("error"),
                    result.get("status"),
                    result.get("encrypt_msg_len", "?"),
                    result.get("forter_token_present"),
                    result.get("feh_count"),
                )
                return None

            logger.info(
                "[CRYPTO] ok  status=%s  encrypt_msg_len=%s  "
                "forter_token=%s  feh_count=%s",
                result.get("status"),
                result.get("encrypt_msg_len"),
                result.get("forter_token_present"),
                result.get("feh_count"),
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
    """Return {encrypt_msg, ctoken, ctoken_ver, fresh_cookies} or None."""
    sync_playwright, PWTimeout = _get_playwright()

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
