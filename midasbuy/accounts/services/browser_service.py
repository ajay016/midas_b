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
    options = {
        "viewport": getattr(
            settings,
            "MIDASBUY_BROWSER_VIEWPORT",
            {"width": 1440, "height": 900},
        ),
    }
    user_agent = getattr(settings, "MIDASBUY_BROWSER_USER_AGENT", "")
    if user_agent:
        options["user_agent"] = user_agent
    return options
