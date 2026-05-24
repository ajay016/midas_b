import logging
from dataclasses import dataclass

from .page_helpers import (
    click_if_visible,
    fill_input,
    get_iframe_by_selector,
    text_contains,
    wait_for_visible,
)
from .selectors import (
    MIDASBUY_CONTINUE_BUTTON,
    MIDASBUY_COOKIE_ACCEPT,
    MIDASBUY_COOKIE_POPUP,
    MIDASBUY_DROPDOWN_SIGN_IN,
    MIDASBUY_EMAIL_INPUT,
    MIDASBUY_KEEP_SIGNED_IN,
    MIDASBUY_LOGIN_IFRAME,
    MIDASBUY_NAV_SIGN_IN,
    MIDASBUY_OPTIONAL_MODAL_CLOSE,
    MIDASBUY_OPTIONAL_MODAL_CLOSE_ALT,
    MIDASBUY_PASSWORD_INPUT,
    MIDASBUY_SIGN_IN_BUTTON,
    MIDASBUY_SIGN_IN_SUCCESS_TEXT,
    MIDASBUY_SUCCESS_CLOSE_BUTTON,
)

logger = logging.getLogger(__name__)


@dataclass
class FlowResult:
    success: bool
    message: str
    step: str


def _safe_log_page_state(page, label: str) -> None:
    try:
        logger.info("[MIDASBUY] %s current_url=%s", label, page.url)
    except Exception:
        logger.exception("[MIDASBUY] failed logging page url for %s", label)

    try:
        html = page.content()
        logger.info("[MIDASBUY] %s page html length=%s", label, len(html))
    except Exception:
        logger.exception("[MIDASBUY] failed logging page html for %s", label)


def _dump_frame_debug(login_iframe) -> None:
    try:
        html = login_iframe.content()
        logger.info("[MIDASBUY] iframe html length=%s", len(html))
        logger.info(
            "[MIDASBUY] iframe markers email_input=%s password_input=%s continue_text=%s signin_text=%s keep_signed_in=%s success_text=%s",
            'autocomplete="username"' in html,
            'type="password"' in html,
            "Continue" in html,
            "SIGN IN" in html,
            "Keep me signed in" in html,
            "SIGN IN SUCCESSFULLY" in html,
        )
    except Exception:
        logger.exception("[MIDASBUY] failed to inspect iframe html")


def close_optional_home_popups(page) -> None:
    for attempt in range(2):
        logger.info("[MIDASBUY] popup close pass=%s", attempt + 1)
        closed_any = False

        if click_if_visible(page, MIDASBUY_OPTIONAL_MODAL_CLOSE_ALT, timeout=700):
            logger.info("[MIDASBUY] closed popup via ALT close button")
            page.wait_for_timeout(200)
            closed_any = True

        if click_if_visible(page, MIDASBUY_OPTIONAL_MODAL_CLOSE, timeout=700):
            logger.info("[MIDASBUY] closed popup via old popup selector")
            page.wait_for_timeout(200)
            closed_any = True

        if click_if_visible(page, "div[class*='close_btn']", timeout=700):
            logger.info("[MIDASBUY] closed popup via generic close button")
            page.wait_for_timeout(200)
            closed_any = True

        if not closed_any:
            logger.info("[MIDASBUY] no optional popup closed in pass=%s", attempt + 1)
            break


def click_sign_in_button(page) -> bool:
    logger.info("[MIDASBUY] trying primary navbar sign-in selector: %s", MIDASBUY_NAV_SIGN_IN)
    if click_if_visible(page, MIDASBUY_NAV_SIGN_IN, timeout=3000):
        logger.info("[MIDASBUY] navbar Sign in clicked via primary selector")
        return True

    logger.info("[MIDASBUY] trying fallback: div[data-id='login']")
    if click_if_visible(page, "div[data-id='login']", timeout=2000):
        logger.info("[MIDASBUY] navbar Sign in clicked via data-id selector")
        return True

    logger.info("[MIDASBUY] trying fallback: div[class*='sign_in']")
    if click_if_visible(page, "div[class*='sign_in']", timeout=2000):
        logger.info("[MIDASBUY] navbar Sign in clicked via class pattern")
        return True

    logger.info("[MIDASBUY] trying fallback: click by text 'Sign in'")
    try:
        sign_in_by_text = page.get_by_text("Sign in", exact=True).first
        if sign_in_by_text.is_visible(timeout=2000):
            sign_in_by_text.click()
            logger.info("[MIDASBUY] navbar Sign in clicked via text match")
            return True
    except Exception as e:
        logger.debug("[MIDASBUY] text click failed: %s", e)

    logger.info("[MIDASBUY] trying JavaScript click on div[data-id='login']")
    try:
        result = page.evaluate("""
            () => {
                const btn = document.querySelector('div[data-id="login"]');
                if (btn) {
                    btn.click();
                    return true;
                }
                return false;
            }
        """)
        if result:
            logger.info("[MIDASBUY] navbar Sign in clicked via JavaScript")
            return True
    except Exception as e:
        logger.debug("[MIDASBUY] JavaScript click failed: %s", e)

    logger.error("[MIDASBUY] all sign-in button strategies failed")
    return False


def click_dropdown_sign_in(page) -> bool:
    logger.info("[MIDASBUY] trying primary dropdown selector: %s", MIDASBUY_DROPDOWN_SIGN_IN)
    if click_if_visible(page, MIDASBUY_DROPDOWN_SIGN_IN, timeout=3000):
        logger.info("[MIDASBUY] dropdown Sign in clicked via primary selector")
        return True

    logger.info("[MIDASBUY] trying fallback: button with text 'Sign in / Sign up'")
    try:
        sign_up_btn = page.get_by_text("Sign in / Sign up", exact=True).first
        if sign_up_btn.is_visible(timeout=2000):
            sign_up_btn.click()
            logger.info("[MIDASBUY] dropdown Sign in clicked via text")
            return True
    except Exception as e:
        logger.debug("[MIDASBUY] text click failed: %s", e)

    logger.info("[MIDASBUY] trying fallback: any button with sign-in text")
    try:
        sidebar_btn = page.locator("div[class*='ulContent'] div[class*='btn_wrap']").first
        if sidebar_btn.is_visible(timeout=2000):
            sidebar_btn.click()
            logger.info("[MIDASBUY] dropdown Sign in clicked via sidebar pattern")
            return True
    except Exception as e:
        logger.debug("[MIDASBUY] sidebar pattern failed: %s", e)

    logger.error("[MIDASBUY] all dropdown sign-in strategies failed")
    return False


def _check_login_success(login_iframe, page) -> bool:
    if text_contains(login_iframe, MIDASBUY_SIGN_IN_SUCCESS_TEXT, "SIGN IN SUCCESSFULLY", timeout=3000):
        logger.info("[MIDASBUY] success modal detected via iframe text")
        return True

    try:
        if not login_iframe.is_visible(timeout=3000):
            logger.info("[MIDASBUY] login iframe disappeared - login likely successful")
            return True
    except Exception:
        pass

    user_selectors = [
        "div[class*='user_mess']",
        "div[class*='avatar']",
        "div[data-id='user-info']",
        "i.i-midas:user-filled",
        "div[class*='user_card']",
    ]

    for selector in user_selectors:
        try:
            if page.locator(selector).first.is_visible(timeout=2000):
                logger.info("[MIDASBUY] user element found: %s", selector)
                return True
        except Exception:
            pass

    try:
        sign_in_btn = page.locator("div[data-id='login']")
        if not sign_in_btn.is_visible(timeout=2000):
            logger.info("[MIDASBUY] sign-in button no longer visible - logged in")
            return True
    except Exception:
        pass

    current_url = page.url
    if "login" not in current_url.lower() and "signin" not in current_url.lower():
        logger.info("[MIDASBUY] URL suggests logged in: %s", current_url)
        return True

    success_selectors = [
        "div[class*='success']",
        "div[class*='icon_text']",
        "p.icon_text",
        "div:has-text('Successfully')",
    ]

    for selector in success_selectors:
        try:
            if login_iframe.locator(selector).first.is_visible(timeout=1000):
                logger.info("[MIDASBUY] success element found: %s", selector)
                close_btn = login_iframe.locator("div.close-btn, div[class*='close']").first
                if close_btn.is_visible(timeout=1000):
                    close_btn.click()
                return True
        except Exception:
            pass

    return False


def _wait_for_email_or_fail(login_iframe) -> bool:
    selectors = [
        MIDASBUY_EMAIL_INPUT,
        'input[type="email"]',
        'input[autocomplete="username"]',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying email selector=%s", selector)
        if wait_for_visible(login_iframe, selector, timeout=1800):
            logger.info("[MIDASBUY] email selector visible=%s", selector)
            return True

    return False


def _fill_email(login_iframe, email: str) -> bool:
    selectors = [
        MIDASBUY_EMAIL_INPUT,
        'input[type="email"]',
        'input[autocomplete="username"]',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying fill email selector=%s", selector)
        if fill_input(login_iframe, selector, email, timeout=1800):
            logger.info("[MIDASBUY] email filled via selector=%s", selector)
            return True

    return False


def _click_continue(login_iframe) -> bool:
    selectors = [
        MIDASBUY_CONTINUE_BUTTON,
        'div.btn.comfirm-btn:has-text("Continue")',
        'text=Continue',
        'button:has-text("Continue")',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying continue selector=%s", selector)
        if click_if_visible(login_iframe, selector, timeout=1800):
            logger.info("[MIDASBUY] Continue clicked via selector=%s", selector)
            return True

    return False


def _wait_for_password(login_iframe) -> bool:
    selectors = [
        MIDASBUY_PASSWORD_INPUT,
        'input[type="password"]',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying password selector=%s", selector)
        if wait_for_visible(login_iframe, selector, timeout=2500):
            logger.info("[MIDASBUY] password selector visible=%s", selector)
            return True

    return False


def _fill_password(login_iframe, password: str) -> bool:
    selectors = [
        MIDASBUY_PASSWORD_INPUT,
        'input[type="password"]',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying fill password selector=%s", selector)
        if fill_input(login_iframe, selector, password, timeout=1800):
            logger.info("[MIDASBUY] password filled via selector=%s", selector)
            return True

    return False


def _click_keep_signed_in(login_iframe) -> None:
    selectors = [
        MIDASBUY_KEEP_SIGNED_IN,
        'div.keep:has-text("Keep me signed in")',
        'div.keep',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying keep-signed-in selector=%s", selector)
        if click_if_visible(login_iframe, selector, timeout=1000):
            logger.info("[MIDASBUY] Keep me signed in clicked via selector=%s", selector)
            return


def _click_sign_in(login_iframe) -> bool:
    selectors = [
        MIDASBUY_SIGN_IN_BUTTON,
        'div.btn.comfirm-btn:has-text("SIGN IN")',
        'text=SIGN IN',
        'button:has-text("SIGN IN")',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying sign-in selector=%s", selector)
        if click_if_visible(login_iframe, selector, timeout=1800):
            logger.info("[MIDASBUY] SIGN IN clicked via selector=%s", selector)
            return True

    return False


def _close_success_modal(login_iframe) -> None:
    selectors = [
        MIDASBUY_SUCCESS_CLOSE_BUTTON,
        'div.close-btn',
        'div[class*="close"]',
    ]

    for selector in selectors:
        logger.info("[MIDASBUY] trying success-close selector=%s", selector)
        if click_if_visible(login_iframe, selector, timeout=1000):
            logger.info("[MIDASBUY] success modal closed via selector=%s", selector)
            return


def run_midasbuy_login_flow(page, account) -> FlowResult:
    logger.info("[MIDASBUY] starting login flow account_id=%s email=%s", account.id, account.email)
    _safe_log_page_state(page, "flow_start")

    page.wait_for_timeout(800)

    close_optional_home_popups(page)

    if wait_for_visible(page, MIDASBUY_COOKIE_POPUP, timeout=1500):
        logger.info("[MIDASBUY] cookie popup visible")
        if click_if_visible(page, MIDASBUY_COOKIE_ACCEPT, timeout=1500):
            logger.info("[MIDASBUY] cookie accept clicked")
            page.wait_for_timeout(300)
        else:
            logger.warning("[MIDASBUY] cookie popup visible but accept click failed")
    else:
        logger.info("[MIDASBUY] cookie popup not shown")

    close_optional_home_popups(page)

    if not click_sign_in_button(page):
        _safe_log_page_state(page, "navbar_signin_failed")
        return FlowResult(False, "Could not click navbar Sign in.", "navbar_sign_in")

    logger.info("[MIDASBUY] navbar Sign in clicked")
    page.wait_for_timeout(400)

    if not click_dropdown_sign_in(page):
        _safe_log_page_state(page, "dropdown_signin_failed")
        return FlowResult(False, "Could not click dropdown Sign in / Sign up.", "dropdown_sign_in")

    logger.info("[MIDASBUY] dropdown Sign in / Sign up clicked")
    page.wait_for_timeout(900)

    logger.info("[MIDASBUY] waiting for login iframe selector=%s", MIDASBUY_LOGIN_IFRAME)
    login_iframe = get_iframe_by_selector(page, MIDASBUY_LOGIN_IFRAME, timeout=5000)
    if not login_iframe:
        logger.error("[MIDASBUY] login iframe not found")
        _safe_log_page_state(page, "iframe_not_found")
        return FlowResult(False, "Login iframe not found.", "login_iframe")

    logger.info("[MIDASBUY] login iframe found")
    page.wait_for_timeout(500)
    _dump_frame_debug(login_iframe)

    logger.info("[MIDASBUY] waiting for email input inside iframe")
    if not _wait_for_email_or_fail(login_iframe):
        logger.error("[MIDASBUY] email input not visible inside iframe")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Email input not visible inside iframe.", "email_input_visible")

    logger.info("[MIDASBUY] filling email=%s", account.email)
    if not _fill_email(login_iframe, account.email):
        logger.error("[MIDASBUY] failed filling email input")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Could not fill email field.", "email_input")

    page.wait_for_timeout(250)

    logger.info("[MIDASBUY] clicking Continue")
    if not _click_continue(login_iframe):
        logger.error("[MIDASBUY] failed clicking Continue")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Could not click Continue button.", "continue_button")

    page.wait_for_timeout(900)
    _dump_frame_debug(login_iframe)

    logger.info("[MIDASBUY] waiting for password field")
    if not _wait_for_password(login_iframe):
        logger.error("[MIDASBUY] password input not visible after Continue")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Password input not visible.", "password_input_visible")

    logger.info("[MIDASBUY] filling password")
    if not _fill_password(login_iframe, account.user_password):
        logger.error("[MIDASBUY] failed filling password")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Could not fill password field.", "password_input")

    page.wait_for_timeout(250)

    logger.info("[MIDASBUY] trying Keep me signed in")
    _click_keep_signed_in(login_iframe)

    page.wait_for_timeout(200)

    logger.info("[MIDASBUY] clicking SIGN IN")
    if not _click_sign_in(login_iframe):
        logger.error("[MIDASBUY] failed clicking SIGN IN")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Could not click SIGN IN button.", "sign_in_button")

    logger.info("[MIDASBUY] SIGN IN clicked, waiting for login completion")
    page.wait_for_timeout(3000)

    if _check_login_success(login_iframe, page):
        logger.info("[MIDASBUY] login successful detected!")

        _close_success_modal(login_iframe)

        page.wait_for_timeout(1000)
        _safe_log_page_state(page, "flow_done")

        logger.info("[MIDASBUY] login flow completed successfully")
        return FlowResult(True, "Midasbuy login flow completed successfully.", "done")
    else:
        try:
            cookies = page.context.cookies()
            if len(cookies) > 0:
                logger.info("[MIDASBUY] Found %s cookies despite no success modal - considering login successful", len(cookies))

                auth_cookies = [
                    c for c in cookies
                    if "session" in c.get("name", "").lower()
                    or "token" in c.get("name", "").lower()
                    or "midas" in c.get("name", "").lower()
                ]
                if auth_cookies:
                    logger.info("[MIDASBUY] Found auth cookies: %s", [c["name"] for c in auth_cookies])
                    return FlowResult(True, "Login successful (verified by cookies).", "done")
        except Exception as e:
            logger.debug("[MIDASBUY] Cookie check failed: %s", e)

        logger.error("[MIDASBUY] login success not detected")
        _dump_frame_debug(login_iframe)
        return FlowResult(False, "Sign-in success not detected.", "sign_in_success")
