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
        # Wait for the iframe element itself to appear in the DOM
        logger.info("[PAGE_HELPERS] waiting for iframe element selector=%s", selector)
        page.wait_for_selector(selector, state="attached", timeout=timeout)
        logger.info("[PAGE_HELPERS] iframe element found in DOM, getting content frame")

        # Use content_frame() — the correct Playwright API to get a Frame from an iframe element
        element_handle = page.query_selector(selector)
        if element_handle:
            frame = element_handle.content_frame()
            if frame:
                logger.info("[PAGE_HELPERS] content_frame() succeeded url=%s", frame.url)
                return frame
            else:
                logger.warning("[PAGE_HELPERS] content_frame() returned None — iframe may not have loaded yet")
                # Give it a moment and retry
                page.wait_for_timeout(1000)
                element_handle = page.query_selector(selector)
                if element_handle:
                    frame = element_handle.content_frame()
                    if frame:
                        logger.info("[PAGE_HELPERS] content_frame() retry succeeded url=%s", frame.url)
                        return frame
        else:
            logger.warning("[PAGE_HELPERS] query_selector returned None for selector=%s", selector)

        # Fallback: scan all frames and return first non-main frame
        logger.warning("[PAGE_HELPERS] falling back to frame scan, total frames=%s", len(page.frames))
        for i, frame in enumerate(page.frames):
            logger.info("[PAGE_HELPERS] frame[%s] url=%s name=%s", i, frame.url, frame.name)
            if frame != page.main_frame:
                logger.info("[PAGE_HELPERS] returning fallback frame[%s]", i)
                return frame

        logger.error("[PAGE_HELPERS] no iframe found for selector=%s", selector)
        return None

    except Exception as e:
        logger.error("[PAGE_HELPERS] get_iframe_by_selector exception selector=%s error=%s", selector, e)

        # Still attempt fallback so we can see what frames exist
        try:
            logger.info("[PAGE_HELPERS] exception fallback — scanning %s frames", len(page.frames))
            for i, frame in enumerate(page.frames):
                logger.info("[PAGE_HELPERS] frame[%s] url=%s name=%s", i, frame.url, frame.name)
            for frame in page.frames:
                if frame != page.main_frame:
                    return frame
        except Exception:
            pass

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
