"""
Midasbuy API service.

Primary path for player lookup: browser-side encryption through the real
window.xMidas VM. The older pure-Python AES guess can produce an encrypt_msg
value, but Midasbuy rejects it because the production algorithm is the VM
output, not a simple token-derived AES transform.
"""
import asyncio
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from typing import Optional

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_APPID = "1450015065"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"
_BROWSER_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="midasbuy-browser")
# Separate thread for the captcha solver — it spins up its own sync_playwright,
# which must not share a thread with the cached session's live Playwright loop.
_SOLVER_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="midasbuy-captcha")
_QUERY_REDEEM_ENDPOINT = "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo"


async def _run_solver_call(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_SOLVER_EXECUTOR, _run_browser_call_sync, func, args)


def _run_browser_call_sync(func, args):
    logger.debug(
        "[SERVICE] browser call thread=%s function=%s",
        current_thread().name,
        getattr(func, "__name__", repr(func)),
    )
    return func(*args)


async def _run_browser_call(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_BROWSER_EXECUTOR, _run_browser_call_sync, func, args)


async def shutdown_browser_worker() -> None:
    from accounts.services.playwright_crypto import close_cached_browser_sessions

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        _BROWSER_EXECUTOR,
        _run_browser_call_sync,
        close_cached_browser_sessions,
        (),
    )
    _BROWSER_EXECUTOR.shutdown(wait=False, cancel_futures=True)
    _SOLVER_EXECUTOR.shutdown(wait=False, cancel_futures=True)


def _looks_like_encrypt_error(data: Optional[dict]) -> bool:
    if not isinstance(data, dict):
        return False
    text = " ".join(
        str(data.get(k, ""))
        for k in ("msg", "err_msg", "error", "err_code", "ret")
    ).lower()
    return "encrypt_msg" in text or "ctoken" in text or "invalid encrypt" in text


async def _api_call(
    payload: dict,
    endpoint: str,
    storage_state_path: Optional[str],
    country_code: str,
    method: str = "POST",
) -> Optional[dict]:
    if not storage_state_path:
        return None

    session_dir = os.path.dirname(storage_state_path)

    browser_only_endpoints = {
        "/interface/getCharac",
        _QUERY_REDEEM_ENDPOINT,
    }

    if endpoint.rstrip("/") in browser_only_endpoints:
        logger.info("[SERVICE] using browser xMidas for endpoint=%s", endpoint)
        from accounts.services.playwright_crypto import call_api_in_browser
        return await _run_browser_call(
            call_api_in_browser,
            payload, endpoint, storage_state_path, country_code, method,
        )

    # ── Primary: pure Python encryption (no browser spin-up) ──────────────────
    xmidas_token_path = os.path.join(session_dir, "xmidas_token.txt")
    page_data_path    = os.path.join(session_dir, "page_data.json")

    if os.path.exists(xmidas_token_path):
        try:
            with open(xmidas_token_path, encoding="utf-8") as f:
                xmidas_token = f.read().strip()

            page_data: dict = {}
            if os.path.exists(page_data_path):
                with open(page_data_path, encoding="utf-8") as f:
                    page_data = json.load(f)

            if xmidas_token:
                from .crypto.crypto import call_api_python
                result = await asyncio.to_thread(
                    call_api_python,
                    payload, endpoint, storage_state_path,
                    country_code, xmidas_token, page_data,
                )
                if result is not None:
                    logger.info(
                        "[SERVICE] python-crypto response  ret=%s  msg=%s  has_page_data=%s",
                        result.get("ret"), result.get("msg"), bool(page_data),
                    )
                    if _looks_like_encrypt_error(result):
                        logger.warning("[SERVICE] python-crypto encrypt rejected - falling back to browser")
                    else:
                        return result
                logger.warning("[SERVICE] python-crypto returned None — falling back to browser")
        except Exception as exc:
            logger.warning("[SERVICE] python-crypto failed (%s) — falling back to browser", exc)

    # ── Fallback: browser-based fetch ─────────────────────────────────────────
    logger.info("[SERVICE] using browser fallback  endpoint=%s", endpoint)
    from accounts.services.playwright_crypto import call_api_in_browser
    return await _run_browser_call(
        call_api_in_browser,
        payload, endpoint, storage_state_path, country_code, method,
    )


# ── Player lookup ─────────────────────────────────────────────────────────────

async def get_player_info(
    player_id: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
    zone_id: str = "",
) -> PlayerLookupResponse:
    if not storage_state_path:
        return PlayerLookupResponse(success=False, error="No session. Please log in first.")

    # The Midasbuy frontend calls /interface/getCharac with the entered PUBG
    # UID as "openid"; app/country/pf are added as public params before xMidas.
    payload = {
        "openid": player_id,
        "zoneid": str(zone_id or "1"),
    }

    data = await _api_call(payload, "/interface/getCharac", storage_state_path, country_code)

    if data is None:
        return PlayerLookupResponse(success=False, error="API request failed. Check logs.")

    if data.get("ret") != 0:
        return PlayerLookupResponse(
            success=False,
            error=data.get("msg") or f"API error ret={data.get('ret')}",
        )

    info = data.get("info", {})
    return PlayerLookupResponse(
        success=True,
        player=PlayerInfo(
            player_id=player_id,
            username=info.get("charac_name") or "",
            role_id=str(info.get("openid") or player_id),
            server_id="",
            zone_id=str(info.get("zoneid") or ""),
        ),
    )


# ── Redeem code info ──────────────────────────────────────────────────────────

def _redeem_query_error_message(data: dict) -> str:
    err_code = str(data.get("err_code") or "")
    msg = data.get("msg") or ""

    messages = {
        "REDEEM_CODE_ALREADY_USED": "Redeem code is already used. Please check the code.",
        "INVALID_REDEEM_CODE": "Invalid redeem code. Please check the code.",
        "QUERY_TOB_REDEEM_CODE_BUSINESS_ERROR": (
            "Midasbuy redeem-code service is busy right now. Please try again later."
        ),
    }

    return messages.get(err_code) or msg or f"Redeem code query failed: {err_code or 'unknown error'}"


def _log_redeem_query_response(data: dict) -> None:
    details = data.get("data", {}).get("details", [])
    detail = details[0] if details and isinstance(details[0], dict) else {}
    debug_id = data.get("data", {}).get("debug_id") or data.get("debug_id")

    logger.info(
        "[REDEEM] Midasbuy response ret=%s code=%s err_code=%s debug_id=%s",
        data.get("ret"),
        data.get("code"),
        data.get("err_code"),
        debug_id,
    )
    logger.debug(
        "[REDEEM] Midasbuy message=%s challenge_type=%s challenge_source=%s",
        data.get("msg"),
        detail.get("error"),
        detail.get("source"),
    )
    logger.debug(
        "[REDEEM] Full Midasbuy response=%s",
        json.dumps(data, ensure_ascii=True, default=str),
    )


def _redeem_product_description(data: dict) -> str:
    products = data.get("redeem_code_info", {}).get("products", [])
    return ", ".join(p.get("name", "") for p in products if p.get("name"))


def _redeem_first_product_id(data: dict) -> str:
    products = data.get("redeem_code_info", {}).get("products", [])
    product = products[0] if products and isinstance(products[0], dict) else {}
    return str(product.get("product_id") or product.get("shelf_product_id") or "")


def _extract_risk_challenge(data: dict) -> tuple[str, str]:
    err_code = str(data.get("err_code") or "")
    if not err_code.startswith("FLEXIBLE_RISK_CONTROL"):
        return "", ""

    details = data.get("data", {}).get("details", [])
    detail = details[0] if details and isinstance(details[0], dict) else {}
    return str(detail.get("error") or ""), str(detail.get("source") or "")


def _get_risk_sdk_url(storage_state_path: str) -> str:
    session_dir = os.path.dirname(storage_state_path)
    server_data_path = os.path.join(session_dir, "server_data.json")
    browser_page_path = os.path.join(session_dir, "browser_page.html")
    sdk_md5 = ""

    if os.path.exists(server_data_path):
        try:
            with open(server_data_path, encoding="utf-8") as file:
                server_data = json.load(file)
            sdk_md5 = str(
                server_data.get("newRiskCtrlComponentOptions", {}).get("flexSdkMd5") or ""
            )
        except (OSError, ValueError, TypeError):
            logger.debug("[REDEEM] could not read risk SDK version from server_data.json")

    if not sdk_md5 and os.path.exists(browser_page_path):
        try:
            with open(browser_page_path, encoding="utf-8") as file:
                html = file.read()
            match = re.search(
                r'"newRiskCtrlComponentOptions"\s*:\s*\{[^}]*"flexSdkMd5"\s*:\s*"([^"]+)"',
                html,
            )
            sdk_md5 = match.group(1) if match else ""
        except OSError:
            logger.debug("[REDEEM] could not read risk SDK version from browser_page.html")

    if sdk_md5:
        return (
            "https://cdn.midasbuy.com/h5/overseah5/js/"
            f"newRiskControlApi.{sdk_md5}.js"
        )

    return "https://cdn.midasbuy.com/h5/overseah5/js/newRiskControlApi.js"


def _redeem_result_error_message(data: Optional[dict]) -> str:
    if not isinstance(data, dict):
        return (
            "Redeem code is valid, but the final confirmation response could "
            "not be verified. Check the account before retrying the same code."
        )

    ret = data.get("ret")
    if ret not in (None, 0, "0"):
        return data.get("msg") or f"Final redemption failed: ret={ret}"

    err_code = data.get("err_code") or data.get("error_code")
    if err_code:
        return data.get("msg") or f"Final redemption failed: {err_code}"

    if data.get("order_no") or data.get("portal_serial_no"):
        logger.info("[REDEEM] final confirmation returned explicit order reference")
        return ""

    pay_info = data.get("payInfo")
    current_bind_user = pay_info.get("currentBindUser") if isinstance(pay_info, dict) else None
    if (
        data.get("pageHandlerName") == "result"
        and data.get("type") == "redeem"
        and data.get("isRedeem") is True
    ):
        logger.warning(
            "[REDEEM] Midasbuy rendered redeem result page without an order "
            "reference; this is not proof of code consumption openid=%s userid=%s",
            current_bind_user.get("openid") if isinstance(current_bind_user, dict) else None,
            current_bind_user.get("userid") if isinstance(current_bind_user, dict) else None,
        )
        return (
            "Midasbuy loaded the redeem result page, but did not return an "
            "order number or portal serial number. The code has not been "
            "confirmed as redeemed."
        )

    logger.warning(
        "[REDEEM] unexpected final confirmation response top_keys=%s pageHandlerName=%s "
        "type=%s isRedeem=%s appid=%s",
        sorted(data.keys())[:60],
        data.get("pageHandlerName"),
        data.get("type"),
        data.get("isRedeem"),
        data.get("appid"),
    )
    return (
        "Midasbuy loaded the result page, but did not return an explicit "
        "redemption confirmation. The code has not been marked as redeemed."
    )


async def query_code_info(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
    zone_id: str = "1",
    rc_token: Optional[str] = None,
    rc_uuid: Optional[str] = None,
) -> RedeemResponse:
    if not storage_state_path:
        return RedeemResponse(success=False, message="No session.")

    clean_code = "".join(pin_code.split())
    payload = {
        "redeem_code": clean_code,
        "open_id": player_id,
        "zone_id": str(zone_id or "1"),
    }
    if rc_token and rc_uuid:
        payload.update(
            {
                "rc_token": rc_token,
                "rc_uuid": rc_uuid,
                "channel": "os_midaspay_v2",
            }
        )
        logger.info("[REDEEM] retrying redeem-code query with completed risk verification")

    data = await _api_call(
        payload,
        _QUERY_REDEEM_ENDPOINT,
        storage_state_path,
        country_code,
    )

    if data is None:
        logger.error("[REDEEM] QueryRedeemCodeInfo returned no response")
        return RedeemResponse(success=False, message="API request failed.")

    _log_redeem_query_response(data)

    ret = data.get("ret", -1)
    if ret != 0:
        challenge_type, challenge_url = _extract_risk_challenge(data)
        if challenge_type == "graphic" and challenge_url:
            # Auto-solve via the paid provider when configured (and we haven't
            # already supplied a token). Falls back to the frontend manual flow.
            if not rc_token:
                try:
                    from accounts.services.captcha_provider import is_enabled as _captcha_enabled
                    from accounts.services.playwright_crypto import obtain_rc_token_via_provider
                except Exception:
                    _captcha_enabled = lambda: False  # noqa: E731
                if _captcha_enabled():
                    logger.info("[REDEEM] graphic risk control — auto-solving via provider")
                    rc = await _run_solver_call(
                        obtain_rc_token_via_provider,
                        challenge_url, storage_state_path, country_code,
                    )
                    if rc and rc.get("rc_token") and rc.get("rc_uuid"):
                        logger.info("[REDEEM] provider produced rc_token — retrying query")
                        return await query_code_info(
                            player_id, pin_code, country_code, storage_state_path,
                            cookies, zone_id, rc["rc_token"], rc["rc_uuid"],
                        )
                    logger.warning("[REDEEM] provider did not produce rc_token — falling back to manual")

            return RedeemResponse(
                success=False,
                message="Security verification is required to continue.",
                verification_required=True,
                challenge_url=challenge_url,
                risk_sdk_url=_get_risk_sdk_url(storage_state_path),
                raw=data,
            )

        return RedeemResponse(
            success=False,
            message=_redeem_query_error_message(data),
            raw=data,
        )

    desc = _redeem_product_description(data)
    if desc:
        message = f"Redeem code query succeeded: {desc}. Final confirmation flow is pending capture."
    else:
        message = "Redeem code query succeeded. Final confirmation flow is pending capture."
    return RedeemResponse(success=True, message=message, raw=data)


# ── Redeem submit ─────────────────────────────────────────────────────────────

async def submit_redeem(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
    zone_id: str = "1",
    rc_token: Optional[str] = None,
    rc_uuid: Optional[str] = None,
    confirm: bool = False,
    product_name: Optional[str] = None,
    product_id: Optional[str] = None,
) -> RedeemResponse:
    if confirm:
        logger.info("[REDEEM] submitting final redeem order through Midasbuy SDK")
        from accounts.services.playwright_crypto import call_redeem_order_in_browser

        result_data = await _run_browser_call(
            call_redeem_order_in_browser,
            {
                "player_id": player_id,
                "pin_code": pin_code,
                "country_code": country_code,
                "appid": _APPID,
                "game_short_url": "pubgm",
                "product_id": product_id or "",
                "product_name": product_name or "",
            },
            storage_state_path,
            country_code,
        )

        result_error = _redeem_result_error_message(result_data)
        raw = {
            "result": result_data,
        }

        if result_error:
            logger.warning("[REDEEM] final confirmation failed/unknown: %s", result_error)
            return RedeemResponse(
                success=False,
                message=result_error,
                raw=raw,
            )

        message = "Redeemed successfully."
        if product_name:
            message = f"Redeemed successfully: {product_name}."

        return RedeemResponse(
            success=True,
            message=message,
            raw=raw,
        )

    check = await query_code_info(
        player_id,
        pin_code,
        country_code,
        storage_state_path,
        cookies,
        zone_id,
        rc_token,
        rc_uuid,
    )
    if not check.success:
        return check

    desc = _redeem_product_description(check.raw or {})
    product_id = _redeem_first_product_id(check.raw or {})
    message = "Redeem code is valid. Please confirm redemption."
    if desc:
        message = f"Redeem code is valid: {desc}. Please confirm redemption."
    return RedeemResponse(
        success=False,
        message=message,
        confirmation_required=True,
        product_name=desc or None,
        product_id=product_id or None,
        raw=check.raw,
    )
