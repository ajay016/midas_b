"""
Midasbuy API service.

All requests are made from *inside* the Playwright browser tab via
call_api_in_browser().  The browser's native window.xMidas SDK generates
a fully fingerprinted encrypt_msg (~1456 chars), and fetch(credentials:'include')
handles cookies + sec-* headers automatically.

Using httpx to send Playwright-generated encrypt_msg fails (HTTP 500) because
headless Playwright produces only ~216-char output — the Tencent Chaos VM
omits Forter/device-signal data that the server validates.
"""
import asyncio
import logging
from typing import Optional

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_APPID = "1900000047"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"


async def _browser_call(
    payload: dict,
    endpoint: str,
    storage_state_path: Optional[str],
    country_code: str,
    method: str = "POST",
) -> Optional[dict]:
    if not storage_state_path:
        return None
    from accounts.services.playwright_crypto import call_api_in_browser
    return await asyncio.to_thread(
        call_api_in_browser,
        payload,
        endpoint,
        storage_state_path,
        country_code,
        method,
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

    payload = {
        "roleId":  player_id,
        "appId":   _APPID,
        "game":    "pubgm",
        "pf":      _PF,
        "country": country_code.upper(),
    }

    data = await _browser_call(payload, "/interface/getCharac", storage_state_path, country_code)

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

    data = await _browser_call(
        payload,
        "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo",
        storage_state_path,
        country_code,
    )

    if data is None:
        return RedeemResponse(success=False, message="API request failed.")

    ret = data.get("ret", -1)
    if ret != 0:
        return RedeemResponse(
            success=False,
            message=data.get("msg") or f"Code error: {data.get('err_code', 'unknown')}",
            raw=data,
        )

    products = data.get("redeem_code_info", {}).get("products", [])
    desc     = ", ".join(p.get("name", "") for p in products) if products else "Unknown reward"
    return RedeemResponse(success=True, message=f"Code valid: {desc}", raw=data)


# ── Redeem submit ─────────────────────────────────────────────────────────────

async def submit_redeem(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> RedeemResponse:
    check = await query_code_info(player_id, pin_code, country_code, storage_state_path, cookies)
    if not check.success:
        return check

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

    data = await _browser_call(
        payload,
        "/interface/shelfProto/shelves_svr/RedeemCode",
        storage_state_path,
        country_code,
    )

    if data is None:
        return RedeemResponse(success=False, message="API request failed.")

    ret = data.get("ret", -1)
    msg = data.get("msg", "")
    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("Redeemed successfully!" if ret == 0 else "Redemption failed"),
        raw=data,
    )
