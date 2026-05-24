"""
Midasbuy API service.

Flow for every API call:
  1. Python reads all cookies (including HttpOnly ctoken) from storage_state.json.
  2. Playwright navigates to the redeem page, runs window.xMidas({d: payload})
     to generate encrypt_msg, and returns it to Python.
  3. Python POSTs {encrypt_msg, ctoken, ctoken_ver} to the API via httpx,
     with all session cookies and browser-like headers.

Key insight: ctoken is an HttpOnly cookie — JavaScript cannot read it via
document.cookie, so we must read it from storage_state.json in Python and
pass it in the request body ourselves.
"""
import asyncio
import json
import logging
from typing import Optional

import httpx

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_BASE  = "https://www.midasbuy.com"
_APPID = "1900000047"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def _load_session(storage_state_path: str) -> tuple[dict, str]:
    """
    Returns (cookies_dict, ctoken_value) from storage_state.json.
    cookies_dict: all midasbuy.com cookies keyed by name.
    ctoken_value: the HttpOnly ctoken cookie value (empty string if missing).
    """
    try:
        with open(storage_state_path, encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        logger.error("[SERVICE] cannot read storage_state: %s", e)
        return {}, ""

    cookies = {}
    ctoken  = ""
    for c in state.get("cookies", []):
        name  = c.get("name", "")
        value = c.get("value", "")
        if not name or not value:
            continue
        if "midasbuy.com" in c.get("domain", ""):
            cookies[name] = value
            if name == "ctoken":
                ctoken = value

    logger.info("[SERVICE] loaded %d cookies, ctoken_found=%s", len(cookies), bool(ctoken))
    return cookies, ctoken


async def _call_api(
    payload: dict,
    api_url: str,
    storage_state_path: str,
    country_code: str,
) -> Optional[dict]:
    """Generate encrypt_msg via Playwright, then POST with httpx + session cookies."""
    from accounts.services.playwright_crypto import get_encrypt_msg

    # Step 1: load cookies and ctoken from storage_state
    cookies, ctoken = _load_session(storage_state_path)
    if not ctoken:
        logger.error("[SERVICE] ctoken not found in storage_state — re-login required")
        return None

    # Step 2: generate encrypt_msg (needs browser for xMidas JS function)
    enc = await asyncio.to_thread(get_encrypt_msg, payload, storage_state_path, country_code)
    if not enc:
        logger.error("[SERVICE] failed to generate encrypt_msg")
        return None

    # Step 3: POST with httpx
    body = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      ctoken,
        "ctoken_ver":  enc["ctoken_ver"],
    }

    referer = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    headers = {
        "Content-Type": "application/json",
        "Accept":        "application/json, text/plain, */*",
        "Origin":        "https://www.midasbuy.com",
        "Referer":       referer,
        "User-Agent":    _UA,
    }

    logger.info("[SERVICE] POST %s ctoken_prefix=%s", api_url, ctoken[:20])

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.post(api_url, json=body, cookies=cookies, headers=headers)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:500])
            return None

        data = resp.json()
        logger.info("[SERVICE] ret=%s", data.get("ret"))
        return data

    except Exception:
        logger.exception("[SERVICE] httpx request failed")
        return None


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

    data = await _call_api(payload, _BASE + "/interface/getCharac", storage_state_path, country_code)

    if data is None:
        return PlayerLookupResponse(success=False, error="Failed to call Midasbuy API. Check session and logs.")

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
    data = await _call_api(payload, url, storage_state_path, country_code)

    if data is None:
        return RedeemResponse(success=False, message="Failed to call Midasbuy API.")

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

    url  = _BASE + "/interface/shelfProto/shelves_svr/RedeemCode"
    data = await _call_api(payload, url, storage_state_path, country_code)

    if data is None:
        return RedeemResponse(success=False, message="Failed to call Midasbuy API.")

    ret = data.get("ret", -1)
    msg = data.get("msg", "")
    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("Redeemed successfully!" if ret == 0 else "Redemption failed"),
        raw=data,
    )
