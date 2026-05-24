import logging

logger = logging.getLogger(__name__)


def click_if_visible(page_or_frame, selector: str, timeout: int = 500) -> bool:
    try:
        locator = page_or_frame.locator(selector).first
        locator.wait_for(state="visible", timeout=timeout)
        locator.click(timeout=timeout)
        return True
    except Exception:
        return False


def fill_input(page_or_frame, selector: str, value: str, timeout: int = 500) -> bool:
    try:
        locator = page_or_frame.locator(selector).first
        locator.wait_for(state="visible", timeout=timeout)
        locator.click(timeout=timeout)
        locator.fill(value, timeout=timeout)
        return True
    except Exception:
        return False


def get_iframe_by_selector(page, selector: str, timeout: int = 5000):
    try:
        frame_locator = page.frame_locator(selector)
        # Verify the iframe is accessible by waiting for its DOM
        frame_locator.locator("body").wait_for(state="attached", timeout=timeout)
        # Return the underlying frame object
        for frame in page.frames:
            element = frame.frame_element()
            try:
                matches = page.locator(selector).first.evaluate(
                    "(el, frame) => el === frame", element
                )
                if matches:
                    return frame
            except Exception:
                continue
        # Fallback: find frame by URL pattern or name
        for frame in page.frames:
            if frame != page.main_frame:
                return frame
        return None
    except Exception as e:
        logger.debug("[PAGE_HELPERS] get_iframe_by_selector failed selector=%s: %s", selector, e)
        return None


def text_contains(page_or_frame, selector: str, text: str, timeout: int = 3000) -> bool:
    try:
        locator = page_or_frame.locator(selector).first
        locator.wait_for(state="visible", timeout=timeout)
        content = locator.text_content(timeout=timeout) or ""
        return text in content
    except Exception:
        return False


def wait_for_visible(page_or_frame, selector: str, timeout: int = 5000) -> bool:
    try:
        page_or_frame.locator(selector).first.wait_for(state="visible", timeout=timeout)
        return True
    except Exception:
        return False
