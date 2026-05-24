"""
Midasbuy API service.

Flow for every API call:
  1. Playwright navigates to the redeem page (using saved storage_state).
  2. JS extracts ctoken from document.cookie and generates encrypt_msg via
     window.xMidas — returns both values to Python.
  3. Python loads all cookies from storage_state.json into an httpx cookie jar.
  4. httpx POST to the API with cookies + {encrypt_msg, ctoken, ctoken_ver}
     and browser-like headers (Origin, Referer, User-Agent, Accept).

Why httpx instead of browser fetch:
  - Browser fetch was getting 500 because the synthetic fetch() call
    didn't include all headers the server expects.
  - httpx lets us set every header explicitly.

Why ctoken from document.cookie (not xMidasToken DOM element):
  - The xMidasToken element holds the SDK's static encryption token, NOT
    the session CSRF token.
  - Midasbuy uses double-submit CSRF: body.ctoken must equal the ctoken
    cookie sent in the Cookie header.  Using the wrong value → 500.
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


def _load_cookies(storage_state_path: str) -> dict:
    """Return all midasbuy.com cookies from storage_state.json as a plain dict."""
    try:
        with open(storage_state_path, encoding="utf-8") as f:
            state = json.load(f)
        return {
            c["name"]: c["value"]
            for c in state.get("cookies", [])
            if c.get("name") and c.get("value")
            and "midasbuy.com" in c.get("domain", "")
        }
    except Exception as e:
        logger.error("[SERVICE] failed to load cookies from %s: %s", storage_state_path, e)
        return {}


async def _call_api(
    payload: dict,
    api_url: str,
    storage_state_path: str,
    country_code: str,
) -> Optional[dict]:
    """
    1. Generate encrypt_msg + ctoken via Playwright (runs in a thread).
    2. POST to api_url with httpx using session cookies.
    """
    from accounts.services.playwright_crypto import get_encrypted_payload

    enc = await asyncio.to_thread(
        get_encrypted_payload, payload, storage_state_path, country_code
    )
    if not enc:
        logger.error("[SERVICE] failed to generate encrypted payload")
        return None

    cookies = _load_cookies(storage_state_path)
    if not cookies:
        logger.error("[SERVICE] no cookies loaded from storage_state")
        return None

    body = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      enc["ctoken"],
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

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.post(api_url, json=body, cookies=cookies, headers=headers)

        logger.info("[SERVICE] httpx %s → status=%s", api_url, resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200 body: %s", resp.text[:500])
            return None

        return resp.json()

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
    data = await _call_api(payload, url, storage_state_path, country_code)

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
    data = await _call_api(payload, url, storage_state_path, country_code)

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
