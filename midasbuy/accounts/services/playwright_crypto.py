"""
Makes Midasbuy API calls from inside a live browser session.

window.xMidas() is Tencent's Chaos VM SDK.  In headless Playwright it produces
only ~216-char output (no fingerprint data); the real browser produces ~1456 chars
because the SDK bundles Forter/device signals.  The server validates fingerprint
size and returns HTTP 500 for the undersized headless output.

Fix: run the ENTIRE request cycle inside the browser page via page.evaluate().
The browser's own window.xMidas generates the authentic fingerprinted payload,
and fetch(credentials:'include') sends it with the real cookies + auto-headers.
"""
import json
import logging
import os
from typing import Optional

_SESSION_STORAGE_JS = """
    (data) => {
        for (const [k, v] of Object.entries(data)) {
            try { sessionStorage.setItem(k, v); } catch(e) {}
        }
    }
"""

logger = logging.getLogger(__name__)

_JS_CALL_API = """
async ({payloadJson, endpoint, method}) => {
    try {
        const tokenEl = document.getElementById('xMidasToken');
        if (!tokenEl || !tokenEl.value) {
            return {error: 'no_xmidas_token'};
        }

        const ctoken     = tokenEl.value;
        const versionEl  = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        if (typeof window.xMidas !== 'function') {
            return {error: 'no_xmidas_function'};
        }

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};
        }

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        const body = JSON.stringify({encrypt_msg, ctoken_ver, ctoken});
        const resp = await fetch('https://www.midasbuy.com' + endpoint, {
            method:      method || 'POST',
            headers:     {
                'Content-Type': 'application/json',
                'Accept':       'application/json, text/plain, */*',
            },
            body:        body,
            credentials: 'include',
        });

        const text = await resp.text();
        let data;
        try { data = JSON.parse(text); }
        catch(e) { return {error: 'invalid_json', status: resp.status, text: text.substring(0, 500)}; }

        return {ok: true, status: resp.status, data: data, encrypt_msg_len: encrypt_msg.length};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""

# Kept for callers that only need encrypt_msg without making an HTTP call
_JS_ENCRYPT_ONLY = """
({payloadJson}) => {
    try {
        const tokenEl   = document.getElementById('xMidasToken');
        const versionEl = document.getElementById('xMidasVersion');

        if (!tokenEl || !tokenEl.value) {
            return {error: 'no_xmidas_token'};
        }

        const ctoken     = tokenEl.value;
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        if (typeof window.xMidas !== 'function') {
            return {error: 'no_xmidas_function'};
        }

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};
        }

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        return {ok: true, ctoken, ctoken_ver, encrypt_msg};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""


def _load_session_storage(storage_state_path: str) -> dict:
    """Load saved sessionStorage data if it exists next to the storage_state file."""
    ss_path = os.path.join(os.path.dirname(storage_state_path), "session_storage.json")
    if not os.path.exists(ss_path):
        return {}
    try:
        with open(ss_path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("[CRYPTO] loaded %d sessionStorage keys from %s", len(data), ss_path)
        return data
    except Exception as e:
        logger.warning("[CRYPTO] could not load session_storage.json: %s", e)
        return {}


def _launch_context(p, storage_state_path: str):
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            # Enable software WebGL/canvas so the Chaos VM gets non-blank fingerprint data
            "--enable-webgl",
            "--use-gl=swiftshader",
            "--ignore-gpu-blocklist",
            "--enable-accelerated-2d-canvas",
            "--enable-features=NetworkService,NetworkServiceInProcess",
        ],
    )

    ss_data = _load_session_storage(storage_state_path)

    context = browser.new_context(
        storage_state=storage_state_path,
        viewport={"width": 1440, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    )
    # Hide automation signals
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
    )
    # Restore Forter blackbox + other sessionStorage before page scripts run
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
        logger.info("[CRYPTO] injected %d sessionStorage keys via init_script", len(ss_data))

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
        logger.warning("[CRYPTO] window.xMidas not ready after 15 s — trying anyway")

    # Wait for the Forter anti-fraud SDK to write its blackbox fingerprint.
    # Without this the Chaos VM reads an empty blackbox → small encrypt_msg → HTTP 500.
    try:
        page.wait_for_function(
            "() => !!window.sessionStorage.getItem('blackbox-selection')",
            timeout=10_000,
        )
        blackbox_len = page.evaluate(
            "() => (window.sessionStorage.getItem('blackbox-selection') || '').length"
        )
        logger.info("[CRYPTO] Forter blackbox-selection ready  len=%d", blackbox_len)
    except PWTimeout:
        logger.warning("[CRYPTO] blackbox-selection not ready — Forter SDK may not have run; encrypt_msg may be small")

    return True


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

    The browser generates a full fingerprinted encrypt_msg (~1456 chars) and
    sends the request with its real cookies + automatic sec-* headers.

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

            logger.info("[CRYPTO] page loaded url=%s", page.url)

            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info(
                "[CRYPTO] calling in-browser fetch  endpoint=%s  keys=%s",
                endpoint,
                list(payload.keys()),
            )

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
                logger.error("[CRYPTO] JS/fetch error: %s", result)
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
    Navigate to the Midasbuy redeem page, call window.xMidas to encrypt the
    payload, and read the ctoken from the xMidasToken DOM element.

    Returns {encrypt_msg, ctoken, ctoken_ver, fresh_cookies} or None on failure.
    NOTE: Use call_api_in_browser() instead when you also need to make the HTTP
    request — the browser generates a properly fingerprinted encrypt_msg there.
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

            logger.info("[CRYPTO] page loaded url=%s", page.url)

            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling window.xMidas for %s", list(payload.keys()))

            result = page.evaluate(_JS_ENCRYPT_ONLY, {"payloadJson": payload_json})

            fresh_cookies = {
                c["name"]: c["value"]
                for c in context.cookies()
                if c.get("name") and c.get("value")
            }
            logger.info("[CRYPTO] fresh cookie count=%d", len(fresh_cookies))

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result:
                logger.error("[CRYPTO] evaluate returned None")
                return None

            if result.get("error"):
                logger.error("[CRYPTO] JS error: %s", result)
                return None

            logger.info(
                "[CRYPTO] ok — ctoken_prefix=%s encrypt_msg_len=%d ctoken_ver=%s",
                result["ctoken"][:20],
                len(result["encrypt_msg"]),
                result["ctoken_ver"],
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
