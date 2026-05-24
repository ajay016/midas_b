"""
Uses Playwright to call window.xMidas() on the live Midasbuy redeem page.

This is the ONLY reliable way to generate a correct encrypt_msg because the
Tencent Chaos VM adds browser fingerprinting data and uses a non-standard
key schedule that can't be cleanly ported to Python.

Flow:
  1. Load existing browser storage_state (session cookies from login).
  2. Navigate to the PUBG Mobile redeem page.
  3. Wait for xmidas-sdk.js to inject xMidasToken into the DOM.
  4. Call window.xMidas({d: JSON.stringify(payload)}) via page.evaluate().
  5. Convert the hex result to base64 (same as the browser's btoa call).
  6. Return {encrypt_msg, ctoken, ctoken_ver}.
"""
import base64
import json
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

_REDEEM_URL = "https://www.midasbuy.com/midasbuy/bd/redeem/pubgm"


def build_encrypted_envelope(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 30_000,
) -> Optional[dict]:
    """
    Returns {encrypt_msg, ctoken, ctoken_ver} or None on failure.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        logger.error("Playwright not installed")
        return None

    redeem_url = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=storage_state_path,
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            try:
                page.goto(redeem_url, timeout=timeout_ms, wait_until="domcontentloaded")
                # Wait for the xMidasToken hidden input to be populated
                page.wait_for_function(
                    "() => !!document.getElementById('xMidasToken')?.value",
                    timeout=timeout_ms,
                )
            except PWTimeout:
                logger.warning("Timeout waiting for xMidasToken on page")
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))

            result = page.evaluate(
                """(payloadJson) => {
                    try {
                        const tokenEl   = document.getElementById('xMidasToken');
                        const versionEl = document.getElementById('xMidasVersion');
                        if (!tokenEl || !tokenEl.value) return {error: 'no_token'};
                        const ctoken     = tokenEl.value;
                        const ctoken_ver = versionEl ? versionEl.value : '1.0.1';
                        const enc = window.xMidas({d: payloadJson});
                        if (!enc || !enc.result) return {error: 'xmidas_failed'};
                        // Convert hex string → bytes → base64  (same as the SDK's btoa call)
                        const bytes = (enc.result.match(/../g) || []).map(h => parseInt(h, 16));
                        const encrypt_msg = btoa(String.fromCharCode(...bytes));
                        return {encrypt_msg, ctoken, ctoken_ver};
                    } catch(e) {
                        return {error: String(e)};
                    }
                }""",
                payload_json,
            )

            browser.close()

            if not result or result.get("error"):
                logger.error("xMidas call failed: %s", result)
                return None

            return result

    except Exception:
        logger.exception("playwright_crypto failed")
        return None
