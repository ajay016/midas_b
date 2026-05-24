"""
Midasbuy API service — pure Python, no Playwright needed for API calls.

Flow:
  1. Load ALL cookies from storage_state.json (session auth).
  2. Encrypt payload with Python AES port of window.xMidas (api.crypto.crypto).
  3. POST {encrypt_msg, ctoken, ctoken_ver} via httpx with session cookies
     and browser-like headers.

ctoken in the request body = the xMidas SDK token from constants.py (static SDK
value that acts as the AES key).  It is NOT a session cookie.
Session auth is done entirely through the Cookie header.
"""
import json
import logging
from typing import Optional

import httpx

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse
from api.crypto.crypto import build_encrypted_payload
from api.crypto.constants import XMIDAS_TOKEN, XMIDAS_VERSION
from accounts.utils import get_xmidas_token_file_path, load_text_file

logger = logging.getLogger(__name__)

_BASE  = "https://www.midasbuy.com"
_APPID = "1900000047"
_PF    = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def _get_xmidas_token(storage_state_path: str, country_code: str = "bd") -> str:
    """
    Return the live xMidasToken (AES key for encrypt_msg).
    1. Try xmidas_token.txt saved during login.
    2. If missing, fetch live from the page via Playwright and cache it.
    3. Fall back to bundled constant as last resort.
    """
    import os
    from accounts.utils import save_text_file as _save

    session_dir = os.path.dirname(storage_state_path)
    token_path  = get_xmidas_token_file_path(session_dir)
    live_token  = load_text_file(token_path)

    if live_token and len(live_token.strip()) >= 64:
        logger.info("[SERVICE] xMidasToken from file  prefix=%s", live_token.strip()[:20])
        return live_token.strip()

    logger.info("[SERVICE] xmidas_token.txt missing — fetching live token via Playwright")
    from accounts.services.playwright_crypto import get_xmidas_token as _fetch
    fetched = _fetch(storage_state_path, country_code)
    if fetched and len(fetched) >= 64:
        _save(token_path, fetched)
        logger.info("[SERVICE] live xMidasToken cached  prefix=%s", fetched[:20])
        return fetched

    logger.warning("[SERVICE] falling back to bundled constant — encrypt_msg may be invalid")
    return XMIDAS_TOKEN


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
    """Encrypt payload with Python AES, then POST via httpx with session cookies."""

    cookies = _load_all_cookies(storage_state_path)
    if not cookies:
        logger.error("[SERVICE] no cookies found in storage_state")
        return None

    xmidas_token = _get_xmidas_token(storage_state_path, country_code)
    body = build_encrypted_payload(payload, xmidas_token, XMIDAS_VERSION)

    referer = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    headers = {
        "Content-Type": "application/json",
        "Accept":        "application/json, text/plain, */*",
        "Origin":        "https://www.midasbuy.com",
        "Referer":       referer,
        "User-Agent":    _UA,
    }

    logger.info(
        "[SERVICE] POST %s  token_prefix=%s  encrypt_msg_len=%d  payload_keys=%s",
        api_url, xmidas_token[:20], len(body["encrypt_msg"]), list(payload.keys()),
    )

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.post(api_url, json=body, cookies=cookies, headers=headers)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200 raw: %s", resp.text[:800])
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
