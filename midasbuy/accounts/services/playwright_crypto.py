"""
Uses Playwright to call window.xMidas() on the live Midasbuy redeem page
and generate the encrypted envelope required for API calls.

The Tencent Chaos VM's xMidas SDK may use a callback-based API, a
synchronous API, or an async/Promise API depending on the SDK version.
This module tries all conventions and logs diagnostics on failure.
"""
import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


# JavaScript that tries every known calling convention for window.xMidas
# and resolves a Promise with the result or an error descriptor.
_XMIDAS_JS = """
(payloadJson) => {
    return new Promise((resolve) => {
        try {
            const tokenEl   = document.getElementById('xMidasToken');
            const versionEl = document.getElementById('xMidasVersion');

            if (!tokenEl || !tokenEl.value) {
                resolve({error: 'no_token', tokenPresent: !!tokenEl});
                return;
            }

            const ctoken     = tokenEl.value;
            const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

            if (typeof window.xMidas !== 'function') {
                const midasKeys = Object.getOwnPropertyNames(window)
                    .filter(k => k.toLowerCase().includes('midas') || k.toLowerCase().includes('xm'));
                resolve({
                    error: 'no_xmidas_function',
                    xMidasType: typeof window.xMidas,
                    midasKeys: midasKeys
                });
                return;
            }

            function finish(hexResult) {
                try {
                    const bytes = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
                    const encrypt_msg = btoa(String.fromCharCode(...bytes));
                    resolve({encrypt_msg, ctoken, ctoken_ver});
                } catch(e) {
                    resolve({error: 'hex_to_b64_failed', detail: String(e)});
                }
            }

            // ── Convention A: callback inside options object ──────────────────
            // xMidas({d: payload, success: fn, fail: fn})
            let cbFired = false;
            try {
                window.xMidas({
                    d: payloadJson,
                    success: function(res) {
                        cbFired = true;
                        if (typeof res === 'string' && res.length > 0) { finish(res); }
                        else if (res && typeof res.result === 'string') { finish(res.result); }
                        else { resolve({error: 'cb_no_result', res: JSON.stringify(res)}); }
                    },
                    fail: function(err) {
                        cbFired = true;
                        resolve({error: 'cb_fail', detail: JSON.stringify(err)});
                    }
                });
            } catch(e) {
                // conv A threw — not this convention
            }

            // Give conv A up to 5 s to fire its callback
            setTimeout(() => {
                if (cbFired) return;

                // ── Convention B: positional callback ─────────────────────────
                // xMidas(successFn, failFn, {d: payload})  OR  xMidas({d:…}, successFn, failFn)
                let cbBFired = false;
                try {
                    window.xMidas(
                        function(res) {
                            cbBFired = true;
                            if (typeof res === 'string' && res.length > 0) { finish(res); }
                            else if (res && typeof res.result === 'string') { finish(res.result); }
                            else { resolve({error: 'cbB_no_result', res: JSON.stringify(res)}); }
                        },
                        function(err) {
                            cbBFired = true;
                            resolve({error: 'cbB_fail', detail: JSON.stringify(err)});
                        },
                        {d: payloadJson}
                    );
                } catch(e) { /* not this convention */ }

                setTimeout(() => {
                    if (cbBFired) return;

                    // ── Convention C: synchronous return ──────────────────────
                    // xMidas({d: payload}) returns the hex string directly
                    // OR an object with .result containing the hex string
                    let enc = null;
                    try { enc = window.xMidas({d: payloadJson}); } catch(e) {}

                    if (typeof enc === 'string' && enc.length > 0) { finish(enc); return; }
                    if (enc && typeof enc.result === 'string' && enc.result.length > 0) { finish(enc.result); return; }

                    // ── Convention D: plain string arg ────────────────────────
                    let enc2 = null;
                    try { enc2 = window.xMidas(payloadJson); } catch(e) {}
                    if (typeof enc2 === 'string' && enc2.length > 0) { finish(enc2); return; }
                    if (enc2 && typeof enc2.result === 'string') { finish(enc2.result); return; }

                    // ── Convention E: parsed object arg ───────────────────────
                    let enc3 = null;
                    try { enc3 = window.xMidas(JSON.parse(payloadJson)); } catch(e) {}
                    if (typeof enc3 === 'string' && enc3.length > 0) { finish(enc3); return; }
                    if (enc3 && typeof enc3.result === 'string') { finish(enc3.result); return; }

                    // All failed — return diagnostics
                    resolve({
                        error: 'all_conventions_failed',
                        encC: JSON.stringify(enc),
                        encD: JSON.stringify(enc2),
                        encE: JSON.stringify(enc3),
                    });
                }, 5000);
            }, 5000);

        } catch(e) {
            resolve({error: 'outer_exception', detail: String(e), stack: (e.stack||'').substring(0,500)});
        }
    });
}
"""


def build_encrypted_envelope(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """
    Returns {encrypt_msg, ctoken, ctoken_ver} or None on failure.
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
                logger.error("[CRYPTO] page.goto timed out url=%s", redeem_url)
                _save_debug(page, session_dir, "crypto_goto_timeout")
                browser.close()
                return None

            logger.info("[CRYPTO] page loaded, url=%s", page.url)

            # ── Step 1: wait for xMidasToken ─────────────────────────────────
            try:
                page.wait_for_function(
                    "() => !!document.getElementById('xMidasToken')?.value",
                    timeout=timeout_ms,
                )
                logger.info("[CRYPTO] xMidasToken element found with value")
            except PWTimeout:
                logger.error("[CRYPTO] timeout waiting for xMidasToken")
                _save_debug(page, session_dir, "crypto_no_token")
                browser.close()
                return None

            # ── Step 2: wait for window.xMidas to be a function ──────────────
            try:
                page.wait_for_function(
                    "() => typeof window.xMidas === 'function'",
                    timeout=15_000,
                )
                logger.info("[CRYPTO] window.xMidas is ready")
            except PWTimeout:
                # Log what IS on the window so we can adapt
                diag = page.evaluate("""() => {
                    const keys = Object.getOwnPropertyNames(window)
                        .filter(k => k.toLowerCase().includes('midas') || k.toLowerCase().includes('xm'));
                    return {
                        xMidasType: typeof window.xMidas,
                        midasKeys: keys,
                        tokenValue: (document.getElementById('xMidasToken')||{}).value?.substring(0,30),
                    };
                }""")
                logger.warning("[CRYPTO] window.xMidas not a function after 15 s, diag=%s", diag)
                # Don't bail yet — let the JS try anyway

            # ── Step 3: call xMidas with all conventions, via Promise ─────────
            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling xMidas with payload_len=%s", len(payload_json))

            # evaluate() resolves Promises automatically in Playwright
            result = page.evaluate(_XMIDAS_JS, payload_json)

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result or result.get("error"):
                logger.error("[CRYPTO] xMidas call failed: %s", result)
                return None

            logger.info(
                "[CRYPTO] success — ctoken_prefix=%s encrypt_msg_len=%s",
                result.get("ctoken", "")[:20],
                len(result.get("encrypt_msg", "")),
            )
            return result

    except Exception:
        logger.exception("[CRYPTO] build_encrypted_envelope crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    """Save screenshot + page HTML for post-mortem debugging."""
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts saved: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)
