"""
Midasbuy API service.

Primary path: pure Python AES-256-CBC encryption using values captured
during login (xmidas_token.txt + page_data.json), sent via httpx.
This avoids the browser entirely and the window.xMidas race condition.

Fallback: Playwright browser tab (call_api_in_browser) for cases where
page_data.json or xmidas_token.txt are missing from the session.
"""
import asyncio
import json
import logging
import os
from typing import Optional

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_APPID = "1900000047"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"


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
                    return result
                logger.warning("[SERVICE] python-crypto returned None — falling back to browser")
        except Exception as exc:
            logger.warning("[SERVICE] python-crypto failed (%s) — falling back to browser", exc)

    # ── Fallback: browser-based fetch ─────────────────────────────────────────
    logger.info("[SERVICE] using browser fallback  endpoint=%s", endpoint)
    from accounts.services.playwright_crypto import call_api_in_browser
    return await asyncio.to_thread(
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

    payload = {
        "roleId":  player_id,
        "appId":   _APPID,
        "game":    "pubgm",
        "pf":      _PF,
        "country": country_code.upper(),
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

    data = await _api_call(
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

    data = await _api_call(
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
