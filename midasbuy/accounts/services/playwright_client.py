import logging
from django.conf import settings

try:
    from patchright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from accounts.utils import (
    get_cookie_file_path,
    get_html_snapshot_file_path,
    get_meta_file_path,
    get_screenshot_file_path,
    get_session_storage_file_path,
    get_storage_state_file_path,
    get_token_file_path,
    get_xmidas_token_file_path,
    save_json_file,
    save_text_file,
)
from .browser_service import get_browser_context_options, get_browser_launch_options
from .login_flow import run_midasbuy_login_flow

logger = logging.getLogger(__name__)


def run_browser_login_session(account, session_dir: str) -> dict:
    screenshot_path       = get_screenshot_file_path(session_dir, "browser_open.png")
    html_snapshot_path    = get_html_snapshot_file_path(session_dir, "browser_page.html")
    storage_state_path    = get_storage_state_file_path(session_dir)
    session_storage_path  = get_session_storage_file_path(session_dir)
    cookie_path           = get_cookie_file_path(session_dir)
    token_path            = get_token_file_path(session_dir)
    xmidas_token_path     = get_xmidas_token_file_path(session_dir)
    meta_path             = get_meta_file_path(session_dir)

    base_url = getattr(
        settings,
        "MIDASBUY_LOGIN_BASE_URL",
        "https://www.midasbuy.com/midasbuy",
    )

    logger.info("[MIDASBUY] browser session start account_id=%s base_url=%s", account.id, base_url)
    logger.info("[MIDASBUY] session_dir=%s", session_dir)

    with sync_playwright() as p:
        browser = p.chromium.launch(**get_browser_launch_options())
        context = browser.new_context(**get_browser_context_options())

        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        page = context.new_page()

        try:
            logger.info("[MIDASBUY] going to base_url")
            page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # Popup handling
            try:
                popup = page.locator("div.MidasbuyUI-pop_content_519c47")
                close_btn = page.locator("div.MidasbuyUI-close_btn_23ba7b")

                if popup.count() > 0:
                    logger.info("[MIDASBUY] popup detected, attempting close")

                    if close_btn.count() > 0:
                        close_btn.first.click(force=True)
                        page.wait_for_timeout(1500)

                        try:
                            popup.wait_for(state="hidden", timeout=8000)
                        except Exception:
                            logger.warning("[MIDASBUY] popup did not fully disappear, continuing anyway")
                    else:
                        logger.warning("[MIDASBUY] popup close button not found")

            except Exception as e:
                logger.warning("[MIDASBUY] popup handling failed: %s", str(e))

            logger.info("[MIDASBUY] landed url=%s", page.url)

            flow_result = run_midasbuy_login_flow(page, account)

            logger.info(
                "[MIDASBUY] flow_result success=%s step=%s message=%s final_url=%s",
                flow_result.success,
                flow_result.step,
                flow_result.message,
                page.url,
            )

            xmidas_token = ""

            if flow_result.success:
                logger.info("[MIDASBUY] Login successful, visiting pages to capture xMidasToken...")

                # Visit general pages first
                for warm_url in [
                    "https://www.midasbuy.com/midasbuy/bd",
                    "https://www.midasbuy.com/midasbuy/bd/shop/pubgm",
                ]:
                    try:
                        page.goto(warm_url, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_timeout(1500)
                    except Exception as e:
                        logger.warning("[MIDASBUY] Failed to visit %s: %s", warm_url, e)

                # Visit redeem page and capture the live xMidasToken
                redeem_url = "https://www.midasbuy.com/midasbuy/bd/redeem/pubgm"
                try:
                    logger.info("[MIDASBUY] Visiting redeem page to capture xMidasToken")
                    page.goto(redeem_url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_function(
                        "() => !!document.getElementById('xMidasToken')?.value",
                        timeout=20000,
                    )
                    xmidas_token = page.evaluate(
                        "document.getElementById('xMidasToken').value"
                    )
                    logger.info("[MIDASBUY] xMidasToken captured: %s...", xmidas_token[:20] if xmidas_token else "EMPTY")

                    # Wait for Forter SDK to finish writing blackbox-selection
                    try:
                        page.wait_for_function(
                            "() => !!window.sessionStorage.getItem('blackbox-selection')",
                            timeout=10_000,
                        )
                        logger.info("[MIDASBUY] Forter blackbox-selection ready")
                    except Exception:
                        logger.warning("[MIDASBUY] blackbox-selection not found after 10 s — saving anyway")

                    # Capture full sessionStorage to restore later in the crypto context
                    try:
                        ss_data = page.evaluate("""
                            () => {
                                const d = {};
                                for (let i = 0; i < sessionStorage.length; i++) {
                                    const k = sessionStorage.key(i);
                                    d[k] = sessionStorage.getItem(k);
                                }
                                return d;
                            }
                        """)
                        save_json_file(session_storage_path, ss_data)
                        logger.info("[MIDASBUY] sessionStorage saved: %d keys", len(ss_data))
                    except Exception as e:
                        logger.warning("[MIDASBUY] Failed to capture sessionStorage: %s", e)

                except Exception as e:
                    logger.warning("[MIDASBUY] Failed to capture xMidasToken: %s", e)

            page.screenshot(path=screenshot_path, full_page=True)
            logger.info("[MIDASBUY] screenshot saved path=%s", screenshot_path)

            html = page.content()
            save_text_file(html_snapshot_path, html)
            logger.info("[MIDASBUY] html snapshot saved path=%s length=%s", html_snapshot_path, len(html))

            storage_state = context.storage_state()
            save_json_file(storage_state_path, storage_state)
            logger.info("[MIDASBUY] storage_state saved path=%s", storage_state_path)

            ctoken_in_storage = None
            for cookie in storage_state.get("cookies", []):
                if cookie.get("name") == "ctoken":
                    ctoken_in_storage = cookie.get("value")
                    logger.info("[MIDASBUY] CToken saved in storage_state: %s...", ctoken_in_storage[:20])
                    break

            if not ctoken_in_storage:
                logger.warning("[MIDASBUY] No ctoken found in storage_state after login")

            cookies = context.cookies()
            save_json_file(cookie_path, cookies)
            logger.info("[MIDASBUY] cookies saved path=%s count=%s", cookie_path, len(cookies))

            if ctoken_in_storage:
                save_text_file(token_path, ctoken_in_storage)
                logger.info("[MIDASBUY] ctoken saved to token file")
            else:
                save_text_file(token_path, "")
                logger.info("[MIDASBUY] token placeholder saved path=%s", token_path)

            save_text_file(xmidas_token_path, xmidas_token)
            logger.info("[MIDASBUY] xmidas_token saved (len=%d) path=%s", len(xmidas_token), xmidas_token_path)

            save_json_file(meta_path, {
                "provider": "midasbuy",
                "base_url": base_url,
                "status": "success" if flow_result.success else "failed",
                "step": flow_result.step,
                "message": flow_result.message,
                "current_url": page.url,
                "title": page.title(),
                "has_ctoken": ctoken_in_storage is not None,
            })

            logger.info("[MIDASBUY] meta saved path=%s", meta_path)

            return {
                "success": flow_result.success,
                "message": flow_result.message,
                "step": flow_result.step,
                "screenshot_path": screenshot_path,
                "html_snapshot_path": html_snapshot_path,
                "storage_state_path": storage_state_path,
                "cookie_path": cookie_path,
                "token_path": token_path,
                "xmidas_token_path": xmidas_token_path,
                "has_ctoken": ctoken_in_storage is not None,
                "has_xmidas_token": bool(xmidas_token),
            }

        except PlaywrightTimeoutError as exc:
            logger.exception("[MIDASBUY] Playwright timeout account_id=%s", account.id)

            try:
                page.screenshot(path=screenshot_path, full_page=True)
                save_text_file(html_snapshot_path, page.content())
            except Exception:
                logger.exception("[MIDASBUY] failed saving debug artifacts after timeout")

            save_json_file(meta_path, {
                "provider": "midasbuy",
                "base_url": base_url,
                "status": "timeout",
                "error": str(exc),
                "current_url": page.url if page else "",
            })

            return {
                "success": False,
                "message": f"Browser open timed out: {exc}",
                "step": "timeout",
                "screenshot_path": screenshot_path,
                "html_snapshot_path": html_snapshot_path,
                "storage_state_path": storage_state_path,
                "cookie_path": cookie_path,
                "token_path": token_path,
                "has_ctoken": False,
            }

        except Exception as exc:
            logger.exception("[MIDASBUY] browser login session failed account_id=%s", account.id)

            try:
                page.screenshot(path=screenshot_path, full_page=True)
                save_text_file(html_snapshot_path, page.content())
            except Exception:
                logger.exception("[MIDASBUY] failed saving debug artifacts after exception")

            save_json_file(meta_path, {
                "provider": "midasbuy",
                "base_url": base_url,
                "status": "error",
                "error": str(exc),
                "current_url": page.url if page else "",
            })

            return {
                "success": False,
                "message": f"Browser login session failed: {exc}",
                "step": "exception",
                "screenshot_path": screenshot_path,
                "html_snapshot_path": html_snapshot_path,
                "storage_state_path": storage_state_path,
                "cookie_path": cookie_path,
                "token_path": token_path,
                "has_ctoken": False,
            }

        finally:
            logger.info("[MIDASBUY] closing browser account_id=%s", account.id)
            browser.close()
