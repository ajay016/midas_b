"""
Generates encrypt_msg for Midasbuy API calls.

The ctoken cookie is HttpOnly so JavaScript can't read it from document.cookie.
Python reads it directly from storage_state.json and passes it separately.
This function only handles the encrypt_msg generation via window.xMidas.
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_JS_ENCRYPT = """
({payloadJson}) => {
    try {
        if (typeof window.xMidas !== 'function') {
            return {error: 'no_xmidas_function'};
        }

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};
        }

        const bytes = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        const versionEl = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        return {ok: true, encrypt_msg, ctoken_ver};
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack || '').substring(0, 500)};
    }
}
"""


def get_xmidas_token(
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 30_000,
) -> Optional[str]:
    """
    Navigate to the redeem page and return the live xMidasToken value.
    Called automatically when xmidas_token.txt is missing from the session dir.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("[CRYPTO] Playwright not installed")
        return None

    redeem_url = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"

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

            logger.info("[CRYPTO] fetching live xMidasToken from %s", redeem_url)
            try:
                page.goto(redeem_url, wait_until="domcontentloaded", timeout=timeout_ms)
                page.wait_for_function(
                    "() => !!document.getElementById('xMidasToken')?.value",
                    timeout=timeout_ms,
                )
                token = page.evaluate("document.getElementById('xMidasToken').value")
                browser.close()
                if token:
                    logger.info("[CRYPTO] live xMidasToken captured len=%d prefix=%s", len(token), token[:20])
                    return token
                logger.error("[CRYPTO] xMidasToken element empty")
                return None
            except PWTimeout:
                logger.error("[CRYPTO] timeout waiting for xMidasToken")
                browser.close()
                return None

    except Exception:
        logger.exception("[CRYPTO] get_xmidas_token crashed")
        return None


def get_encrypt_msg(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page and generate encrypt_msg via window.xMidas.

    Returns {encrypt_msg, ctoken_ver} or None on failure.
    ctoken is NOT returned here — caller reads it from storage_state.json
    because ctoken is HttpOnly and invisible to JavaScript.
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
                "[CRYPTO] encrypt_msg_len=%s ctoken_ver=%s",
                len(result["encrypt_msg"]),
                result["ctoken_ver"],
            )
            return {
                "encrypt_msg": result["encrypt_msg"],
                "ctoken_ver":  result["ctoken_ver"],
            }

    except Exception:
        logger.exception("[CRYPTO] get_encrypt_msg crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)
