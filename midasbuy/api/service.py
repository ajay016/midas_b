"""
Midasbuy API service.

For every call:
  1. Playwright navigates to the redeem page (using saved storage_state),
     calls window.xMidas({d: JSON.stringify(payload)}) to get encrypt_msg,
     and reads ctoken from document.getElementById('xMidasToken').value.
  2. Python loads all session cookies from storage_state.json.
  3. httpx POSTs {encrypt_msg, ctoken, ctoken_ver} with session cookies and
     browser-like headers (Origin, Referer, User-Agent, Accept).

Why Playwright for encrypt_msg:
  window.xMidas is an obfuscated Tencent SDK.  Our Python AES port produced
  a different ciphertext length (236 vs 216 chars) — the algorithm or key
  schedule is not a simple AES-256-CBC.  The browser always gets it right.

Why httpx for the HTTP call:
  Browser-internal fetch() was getting HTTP 500 because it didn't include all
  required headers.  httpx lets us set Origin, Referer, User-Agent explicitly.
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


def _load_all_cookies(storage_state_path: str) -> dict:
    """Load every cookie from storage_state.json — no domain filter."""
    try:
        with open(storage_state_path, encoding="utf-8") as f:
            state = json.load(f)
        cookies = {
            c["name"]: c["value"]
            for c in state.get("cookies", [])
            if c.get("name") and c.get("value")
        }
        logger.info("[SERVICE] loaded %d cookies from storage_state", len(cookies))
        return cookies
    except Exception as e:
        logger.error("[SERVICE] cannot read storage_state: %s", e)
        return {}


async def _call_api(
    payload: dict,
    api_url: str,
    storage_state_path: str,
    country_code: str,
) -> Optional[dict]:
    """
    1. Use Playwright to generate encrypt_msg + ctoken from the live browser.
    2. Load session cookies from storage_state.json.
    3. POST via httpx with cookies + encrypted body + browser headers.
    """
    from accounts.services.playwright_crypto import get_browser_payload

    enc = await asyncio.to_thread(
        get_browser_payload, payload, storage_state_path, country_code
    )
    if not enc:
        logger.error("[SERVICE] failed to generate browser payload")
        return None

    cookies = _load_all_cookies(storage_state_path)
    if not cookies:
        logger.error("[SERVICE] no cookies in storage_state")
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

    logger.info(
        "[SERVICE] POST %s  ctoken_prefix=%s  encrypt_msg_len=%d",
        api_url, enc["ctoken"][:20], len(enc["encrypt_msg"]),
    )

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.post(api_url, json=body, cookies=cookies, headers=headers)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200 body: %s", resp.text[:800])
            return None

        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)
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
        return PlayerLookupResponse(success=False, error="Failed to call Midasbuy API. Check logs.")

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
