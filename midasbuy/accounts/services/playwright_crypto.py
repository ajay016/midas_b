"""
Generates the encrypted payload (encrypt_msg + ctoken) needed by Midasbuy APIs.

Flow:
  1. Load stored session into headless browser.
  2. Navigate to redeem page so the xMidas SDK loads.
  3. Get ctoken from document.cookie (the session CSRF token — must match the
     ctoken cookie sent in the request headers).
  4. Generate encrypt_msg: window.xMidas({d: JSON.stringify(payload)}) returns
     a hex string; convert hex bytes → base64.
  5. Return {encrypt_msg, ctoken, ctoken_ver} to Python caller.

The actual HTTP request is made by the Python caller using httpx with cookies
loaded from storage_state.json.  We never make the API call from inside the
browser — that was the old broken approach.
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Returns the encrypted payload values; no fetch() call here.
_JS_ENCRYPT = """
({payloadJson}) => {
    try {
        // ctoken in the request body MUST equal the ctoken cookie
        // (double-submit CSRF pattern — server rejects if they differ)
        function parseCookie(name) {
            const v = '; ' + document.cookie;
            const p = v.split('; ' + name + '=');
            return p.length >= 2 ? decodeURIComponent(p.pop().split(';').shift()) : '';
        }

        const ctoken = parseCookie('ctoken');
        if (!ctoken) {
            return {error: 'no_ctoken_cookie', cookies_preview: document.cookie.substring(0, 300)};
        }

        const versionEl = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        if (typeof window.xMidas !== 'function') {
            return {error: 'no_xmidas_function'};
        }

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};
        }

        const bytes = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        return {
            ok: true,
            ctoken,
            ctoken_ver,
            encrypt_msg,
        };
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""


def get_encrypted_payload(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page, extract ctoken from session cookies,
    and generate encrypt_msg via window.xMidas.

    Returns dict with keys {encrypt_msg, ctoken, ctoken_ver}, or None on failure.
    Does NOT make any API call — the caller uses httpx for that.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("[CRYPTO] Playwright not installed")
        return None

    redeem_url = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            context = browser.new_context(
                storage_state=storage_state_path,
                viewport={"width": 1440, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            )
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            )
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

            # Wait for window.xMidas
            try:
                page.wait_for_function(
                    "() => typeof window.xMidas === 'function'",
                    timeout=timeout_ms,
                )
                logger.info("[CRYPTO] window.xMidas ready")
            except PWTimeout:
                logger.warning("[CRYPTO] window.xMidas not ready — trying anyway")

            payload_json = json.dumps(payload, separators=(",", ":"))
            result = page.evaluate(_JS_ENCRYPT, {"payloadJson": payload_json})

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result:
                logger.error("[CRYPTO] evaluate returned None")
                return None

            if result.get("error"):
                logger.error("[CRYPTO] JS error: %s", result)
                return None

            logger.info(
                "[CRYPTO] encrypted — ctoken_prefix=%s encrypt_msg_len=%s ctoken_ver=%s",
                result["ctoken"][:20],
                len(result["encrypt_msg"]),
                result["ctoken_ver"],
            )
            return {
                "encrypt_msg": result["encrypt_msg"],
                "ctoken":      result["ctoken"],
                "ctoken_ver":  result["ctoken_ver"],
            }

    except Exception:
        logger.exception("[CRYPTO] get_encrypted_payload crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)
