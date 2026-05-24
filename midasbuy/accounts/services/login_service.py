from dataclasses import dataclass
import logging
from typing import Optional

from django.conf import settings
from django.utils import timezone

from accounts.models import MidasbuyAccount, MidasbuyLoginAttempt
from accounts.utils import (
    ensure_clean_session_dir,
    get_cookie_file_path,
    get_midasbuy_session_dir,
    get_storage_state_file_path,
    get_token_file_path,
    load_json_file,
)
from .playwright_client import run_browser_login_session


logger = logging.getLogger(__name__)


@dataclass
class LoginResult:
    success: bool
    message: str
    session_dir: Optional[str] = None
    cookie_path: Optional[str] = None
    storage_state_path: Optional[str] = None
    token_path: Optional[str] = None
    screenshot_path: Optional[str] = None
    html_snapshot_path: Optional[str] = None
    cookie_data: Optional[list] = None
    storage_state_data: Optional[dict] = None


def login_midasbuy_account(account: MidasbuyAccount) -> LoginResult:
    logger.info(
        "[MIDASBUY] login_midasbuy_account start account_id=%s email=%s",
        account.id,
        account.email,
    )

    session_dir = get_midasbuy_session_dir(settings.BASE_DIR, account.id)
    logger.info("[MIDASBUY] session_dir=%s", session_dir)

    ensure_clean_session_dir(session_dir)
    logger.info("[MIDASBUY] session dir cleaned")

    browser_result = run_browser_login_session(account, session_dir)
    logger.info("[MIDASBUY] browser_result=%s", browser_result)

    cookie_path = get_cookie_file_path(session_dir)
    storage_state_path = get_storage_state_file_path(session_dir)
    token_path = get_token_file_path(session_dir)

    logger.info(
        "[MIDASBUY] expected files cookie=%s storage=%s token=%s",
        cookie_path,
        storage_state_path,
        token_path,
    )

    cookie_data = load_json_file(cookie_path) or []
    storage_state_data = load_json_file(storage_state_path) or {}

    logger.info(
        "[MIDASBUY] loaded cookie_count=%s storage_state_keys=%s",
        len(cookie_data),
        list(storage_state_data.keys()) if isinstance(storage_state_data, dict) else [],
    )

    result = LoginResult(
        success=browser_result["success"],
        message=browser_result["message"],
        session_dir=session_dir,
        cookie_path=cookie_path,
        storage_state_path=storage_state_path,
        token_path=token_path,
        screenshot_path=browser_result.get("screenshot_path"),
        html_snapshot_path=browser_result.get("html_snapshot_path"),
        cookie_data=cookie_data,
        storage_state_data=storage_state_data,
    )

    logger.info(
        "[MIDASBUY] login_midasbuy_account end account_id=%s success=%s message=%s",
        account.id,
        result.success,
        result.message,
    )
    return result


def apply_login_result(account: MidasbuyAccount, result: LoginResult) -> None:
    logger.info(
        "[MIDASBUY] apply_login_result start account_id=%s success=%s",
        account.id,
        result.success,
    )

    if result.success:
        account.status = 1
        account.last_error = ""
        account.last_login_at = timezone.now()
        account.session_path = result.cookie_path
        account.storage_state_path = result.storage_state_path
        account.token_path = result.token_path
        account.cookie_data = result.cookie_data or []
        account.storage_state_data = result.storage_state_data or {}
    else:
        account.status = 2
        account.last_error = result.message

    account.save(
        update_fields=[
            "status",
            "last_error",
            "last_login_at",
            "session_path",
            "storage_state_path",
            "token_path",
            "cookie_data",
            "storage_state_data",
            "updated_at",
        ]
    )

    logger.info(
        "[MIDASBUY] account saved account_id=%s status=%s session_path=%s",
        account.id,
        account.status,
        account.session_path,
    )

    MidasbuyLoginAttempt.objects.create(
        account=account,
        result="success" if result.success else "failed",
        message=result.message,
        screenshot_path=result.screenshot_path,
        html_snapshot_path=result.html_snapshot_path,
    )

    logger.info("[MIDASBUY] login attempt row created account_id=%s", account.id)


def login_account_and_persist(account: MidasbuyAccount) -> LoginResult:
    logger.info("[MIDASBUY] login_account_and_persist called account_id=%s", account.id)
    result = login_midasbuy_account(account)
    apply_login_result(account, result)
    logger.info(
        "[MIDASBUY] login_account_and_persist finished account_id=%s success=%s",
        account.id,
        result.success,
    )
    return result
