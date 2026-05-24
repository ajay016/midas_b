"""
Uses Playwright to encrypt a payload via window.xMidas AND make the API
call FROM WITHIN the same browser session.

This is required because Midasbuy validates that the ctoken, cookies, and
browser fingerprint all come from the same context. An httpx request made
from outside the browser will always get a 500 because the session and
fingerprint don't match.

Flow:
  1. Load stored session (storage_state) into a headless browser.
  2. Navigate to the PUBG Mobile redeem page to load the xMidas SDK.
  3. Generate encrypt_msg: hexResult = window.xMidas({d: JSON.stringify(payload)})
     then base64-encode the hex bytes.
  4. POST to the target API URL using fetch() from inside the browser.
  5. Return the parsed JSON response.
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

_JS = """
async ({payloadJson, apiUrl}) => {
    try {
        // ── get ctoken from DOM ───────────────────────────────────────
        const tokenEl   = document.getElementById('xMidasToken');
        const versionEl = document.getElementById('xMidasVersion');
        if (!tokenEl || !tokenEl.value) {
            return {error: 'no_token'};
        }
        const ctoken     = tokenEl.value;
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        // ── generate encrypt_msg via window.xMidas ────────────────────
        if (typeof window.xMidas !== 'function') {
            return {error: 'no_xmidas_function', type: typeof window.xMidas};
        }

        const hexResult = window.xMidas({d: payloadJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};
        }

        const bytes = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        // ── POST to Midasbuy API from inside the browser ──────────────
        // This ensures cookies, fingerprint, and ctoken all match the
        // same session — which an external httpx call cannot replicate.
        const resp = await fetch(apiUrl, {
            method:  'POST',
            headers: {'Content-Type': 'application/json'},
            body:    JSON.stringify({encrypt_msg, ctoken, ctoken_ver}),
        });

        const text = await resp.text();
        let data;
        try   { data = JSON.parse(text); }
        catch { data = {raw_text: text.substring(0, 500)}; }

        return {
            http_status: resp.status,
            data:        data,
            debug: {
                ctoken_prefix:    ctoken.substring(0, 20),
                encrypt_msg_len:  encrypt_msg.length,
                api_url:          apiUrl,
            },
        };

    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack||'').substring(0, 500)};
    }
}
"""


def call_api_via_browser(
    payload: dict,
    api_url: str,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Encrypt payload via window.xMidas and POST to api_url from inside
    the same Playwright browser session.

    Returns the parsed JSON response dict, or None on failure.
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

            # Wait for window.xMidas
            try:
                page.wait_for_function(
                    "() => typeof window.xMidas === 'function'",
                    timeout=15_000,
                )
                logger.info("[CRYPTO] window.xMidas ready")
            except PWTimeout:
                logger.warning("[CRYPTO] window.xMidas not ready after 15 s — trying anyway")

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling xMidas + fetch to %s", api_url)

            result = page.evaluate(_JS, {"payloadJson": payload_json, "apiUrl": api_url})

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result:
                logger.error("[CRYPTO] evaluate returned None")
                return None

            if result.get("error"):
                logger.error("[CRYPTO] JS error: %s", result)
                return None

            debug = result.get("debug", {})
            logger.info(
                "[CRYPTO] browser fetch done — http_status=%s ctoken_prefix=%s encrypt_msg_len=%s",
                result.get("http_status"),
                debug.get("ctoken_prefix"),
                debug.get("encrypt_msg_len"),
            )

            data = result.get("data", {})
            if result.get("http_status") != 200:
                logger.error("[CRYPTO] non-200 from API: status=%s data=%s", result.get("http_status"), data)
                return None

            logger.info("[CRYPTO] API response: ret=%s", data.get("ret"))
            return data

    except Exception:
        logger.exception("[CRYPTO] call_api_via_browser crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)
