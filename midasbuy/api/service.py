"""
Midasbuy API service.

All Midasbuy API calls are made FROM WITHIN a Playwright browser session
so that cookies, ctoken, and browser fingerprint are consistent.
An external httpx request always gets HTTP 500 because the server
validates that these three things come from the same browser context.

Endpoints:
  Player lookup : POST /interface/getCharac
  Code info     : POST /interface/shelfProto/shelves_svr/QueryRedeemCodeInfo
  Redeem        : POST /interface/shelfProto/shelves_svr/RedeemCode
"""
import asyncio
import logging
from typing import Optional

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_BASE  = "https://www.midasbuy.com"
_APPID = "1900000047"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"


def _no_session() -> None:
    pass  # placeholder so the import stays clean


async def _browser_call(
    payload: dict,
    api_url: str,
    storage_state_path: Optional[str],
    country_code: str,
) -> Optional[dict]:
    """Run call_api_via_browser in a thread (sync Playwright can't run in event loop)."""
    if not storage_state_path:
        return None
    from accounts.services.playwright_crypto import call_api_via_browser
    return await asyncio.to_thread(call_api_via_browser, payload, api_url, storage_state_path, country_code)


async def get_player_info(
    player_id: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> PlayerLookupResponse:
    if not storage_state_path:
        return PlayerLookupResponse(success=False, error="No session. Please log in to a Midasbuy account first.")

    payload = {
        "roleId":  player_id,
        "appId":   _APPID,
        "game":    "pubgm",
        "pf":      _PF,
        "country": country_code.upper(),
    }

    data = await _browser_call(payload, _BASE + "/interface/getCharac", storage_state_path, country_code)

    if data is None:
        return PlayerLookupResponse(success=False, error="Failed to call Midasbuy API. Check session and logs.")

    logger.info("[SERVICE] getCharac ret=%s", data.get("ret"))

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
            role_id=info.get("openid") or player_id,
            server_id="",
            zone_id=str(info.get("zoneid") or ""),
        ),
    )


async def query_code_info(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> RedeemResponse:
    if not storage_state_path:
        return RedeemResponse(success=False, message="No session.")

    payload = {
        "roleId":  player_id,
        "appId":   _APPID,
        "game":    "pubgm",
        "pf":      _PF,
        "country": country_code.upper(),
        "code":    pin_code,
        "channel": "MIDASBUY_REDEEM",
    }

    url  = _BASE + "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo"
    data = await _browser_call(payload, url, storage_state_path, country_code)

    if data is None:
        return RedeemResponse(success=False, message="Failed to call Midasbuy API.")

    logger.info("[SERVICE] QueryRedeemCodeInfo ret=%s", data.get("ret"))

    ret = data.get("ret", -1)
    if ret != 0:
        return RedeemResponse(
            success=False,
            message=data.get("msg") or f"Code error: {data.get('err_code', 'unknown')}",
            raw=data,
        )

    products = data.get("redeem_code_info", {}).get("products", [])
    desc = ", ".join(p.get("name", "") for p in products) if products else "Unknown reward"
    return RedeemResponse(success=True, message=f"Code valid: {desc}", raw=data)


async def submit_redeem(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> RedeemResponse:
    # Step 1: validate code
    check = await query_code_info(player_id, pin_code, country_code, storage_state_path, cookies)
    if not check.success:
        return check

    # Step 2: redeem
    payload = {
        "roleId":    player_id,
        "appId":     _APPID,
        "game":      "pubgm",
        "pf":        _PF,
        "country":   country_code.upper(),
        "code":      pin_code,
        "channel":   "MIDASBUY_REDEEM",
        "channelId": "MIDASBUY_REDEEM",
    }

    url  = _BASE + "/interface/shelfProto/shelves_svr/RedeemCode"
    data = await _browser_call(payload, url, storage_state_path, country_code)

    if data is None:
        return RedeemResponse(success=False, message="Failed to call Midasbuy API.")

    logger.info("[SERVICE] RedeemCode ret=%s", data.get("ret"))

    ret = data.get("ret", -1)
    msg = data.get("msg", "")
    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("Redeemed successfully!" if ret == 0 else "Redemption failed"),
        raw=data,
    )
