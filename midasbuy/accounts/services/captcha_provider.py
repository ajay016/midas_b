"""
Paid captcha provider clients (Tencent TCaptcha / TenDI).

Default provider: 2Captcha (TencentTaskProxyless) — solves on their own clean
infrastructure and returns {ticket, randstr}, which sidesteps our device-
fingerprint / IP frequency penalty.

Config (env):
  CAPTCHA_PROVIDER   = "2captcha"   (default)
  CAPTCHA_API_KEY    = "<your key>" (required to enable the paid path)
  CAPTCHA_APP_ID     = "188937037"  (TCaptcha aid from the slider URL)

Zero extra deps — uses urllib from the stdlib.
"""
import json
import logging
import os
import time
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

_2CAPTCHA_BASE = os.getenv("CAPTCHA_2CAPTCHA_BASE", "https://api.2captcha.com")
_DEFAULT_APP_ID = os.getenv("CAPTCHA_APP_ID", "188937037")


def _post_json(url: str, payload: dict, timeout: int = 30) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def solve_tencent_2captcha(
    api_key: str,
    app_id: str,
    website_url: str,
    *,
    poll_timeout: int = 180,
    poll_interval: int = 5,
    retries: int = 3,
) -> Optional[dict]:
    """
    Solve Tencent TCaptcha via 2Captcha. Returns {'ticket','randstr','appid'} or None.
    Retries on ERROR_CAPTCHA_UNSOLVABLE (often transient / worker-dependent).
    """
    # Our site uses the GLOBAL TCaptcha, not the mainland turing.captcha default —
    # passing the wrong script makes 2Captcha render a different captcha and fail.
    captcha_script = os.getenv(
        "CAPTCHA_SCRIPT", "https://global.captcha.gtimg.com/TCaptcha-global.js"
    )
    for attempt in range(1, retries + 1):
        try:
            task = {
                "type": "TencentTaskProxyless",
                "appId": str(app_id),
                "websiteURL": website_url,
            }
            if captcha_script:
                task["captchaScript"] = captcha_script
            created = _post_json(f"{_2CAPTCHA_BASE}/createTask", {
                "clientKey": api_key,
                "task": task,
            })
            if created.get("errorId"):
                logger.error("[CAPTCHA] 2captcha createTask error: %s", created)
                return None
            task_id = created.get("taskId")
            logger.info("[CAPTCHA] 2captcha task created id=%s (attempt %d/%d)", task_id, attempt, retries)

            deadline = time.time() + poll_timeout
            unsolvable = False
            while time.time() < deadline:
                time.sleep(poll_interval)
                res = _post_json(f"{_2CAPTCHA_BASE}/getTaskResult", {
                    "clientKey": api_key, "taskId": task_id,
                })
                err = res.get("errorCode") or ""
                if err == "ERROR_CAPTCHA_UNSOLVABLE":
                    logger.warning("[CAPTCHA] 2captcha unsolvable (attempt %d/%d) — retrying", attempt, retries)
                    unsolvable = True
                    break
                if res.get("errorId"):
                    logger.error("[CAPTCHA] 2captcha getTaskResult error: %s", res)
                    return None
                if res.get("status") == "ready":
                    sol = res.get("solution", {}) or {}
                    logger.info(
                        "[CAPTCHA] 2captcha solved ret=%s cost=%s ticket_len=%s",
                        sol.get("ret"), res.get("cost"), len(str(sol.get("ticket") or "")),
                    )
                    return {
                        "ret": sol.get("ret", 0),
                        "ticket": sol.get("ticket"),
                        "randstr": sol.get("randstr"),
                        "appid": sol.get("appid") or app_id,
                    }
                logger.info("[CAPTCHA] 2captcha task pending...")
            if not unsolvable:
                logger.error("[CAPTCHA] 2captcha timed out after %ss", poll_timeout)
                return None
        except Exception:
            logger.exception("[CAPTCHA] 2captcha solve failed")
            return None
    logger.error("[CAPTCHA] 2captcha could not solve after %d attempts", retries)
    return None


def is_enabled() -> bool:
    return bool(os.getenv("CAPTCHA_API_KEY"))


def solve_tencent(website_url: str, app_id: Optional[str] = None) -> Optional[dict]:
    """
    Provider-agnostic entry point. Returns {'ticket','randstr','appid'} or None.
    Enabled only when CAPTCHA_API_KEY is set.
    """
    api_key = os.getenv("CAPTCHA_API_KEY", "")
    if not api_key:
        return None
    provider = os.getenv("CAPTCHA_PROVIDER", "2captcha").lower()
    app_id = app_id or _DEFAULT_APP_ID

    if provider in ("2captcha", "twocaptcha"):
        return solve_tencent_2captcha(api_key, app_id, website_url)

    logger.error("[CAPTCHA] unknown CAPTCHA_PROVIDER=%s (supported: 2captcha)", provider)
    return None
