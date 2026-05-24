from django.conf import settings


def get_browser_launch_options() -> dict:
    return {
        "headless": getattr(settings, "MIDASBUY_BROWSER_HEADLESS", True),
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    }


def get_browser_context_options() -> dict:
    return {
        "user_agent": getattr(
            settings,
            "MIDASBUY_BROWSER_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ),
        "viewport": getattr(
            settings,
            "MIDASBUY_BROWSER_VIEWPORT",
            {"width": 1440, "height": 900},
        ),
    }
