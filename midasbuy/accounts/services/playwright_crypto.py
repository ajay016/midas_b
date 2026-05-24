"""
Generates the Midasbuy API request payload from inside a live browser session.

window.xMidas() is Tencent's obfuscated SDK — reverse-engineering it in Python
has proven unreliable (wrong ciphertext length/format).  Instead we let the
browser generate the correct encrypt_msg and read the real ctoken from the DOM,
then hand both back to Python so httpx can make the actual HTTP request with
all session cookies and proper headers.

Returned dict: {encrypt_msg, ctoken, ctoken_ver}
  - encrypt_msg : base64 output of window.xMidas({d: JSON.stringify(payload)})
  - ctoken      : document.getElementById('xMidasToken').value  (SDK CSRF token)
  - ctoken_ver  : document.getElementById('xMidasVersion').value or '1.0.1'
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_JS = """
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

        return {
            ok:          true,
            ctoken:      ctoken,
            ctoken_ver:  ctoken_ver,
            encrypt_msg: encrypt_msg,
        };
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""


def get_browser_payload(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page, call window.xMidas to encrypt the
    payload, and read the ctoken from the xMidasToken DOM element.

    Returns {encrypt_msg, ctoken, ctoken_ver} or None on failure.
    The actual HTTP request is made by the caller using httpx + session cookies.
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

            # Wait for xMidasToken to have a value
            try:
                page.wait_for_function(
                    "() => !!document.getElementById('xMidasToken')?.value",
                    timeout=timeout_ms,
                )
                logger.info("[CRYPTO] xMidasToken ready")
            except PWTimeout:
                logger.error("[CRYPTO] timeout waiting for xMidasToken")
                _save_debug(page, session_dir, "crypto_no_token")
                browser.close()
                return None

            # Wait for window.xMidas function
            try:
                page.wait_for_function(
                    "() => typeof window.xMidas === 'function'",
                    timeout=15_000,
                )
                logger.info("[CRYPTO] window.xMidas ready")
            except PWTimeout:
                logger.warning("[CRYPTO] window.xMidas not ready after 15 s — trying anyway")

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling window.xMidas for %s", list(payload.keys()))

            result = page.evaluate(_JS, {"payloadJson": payload_json})

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
                "encrypt_msg": result["encrypt_msg"],
                "ctoken":      result["ctoken"],
                "ctoken_ver":  result["ctoken_ver"],
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
