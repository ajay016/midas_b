"""
Midasbuy API service.

For every call:
  1. Playwright navigates to the redeem page (using saved storage_state),
     calls window.xMidas({d: JSON.stringify(payload)}) to get encrypt_msg,
     and reads ctoken from document.getElementById('xMidasToken').value.
  2. Python loads all session cookies from storage_state.json.
  3. httpx sends the request with session cookies and browser-like headers.

Player lookup  → GET  /interface/queryRoleDetail   (encrypt_msg as query params)
Code check     → POST /interface/shelfProto/shelves_svr/QueryRedeemCodeInfo
Redeem submit  → POST /interface/shelfProto/shelves_svr/RedeemCode

Why Playwright for encrypt_msg:
  window.xMidas is an obfuscated Tencent Chaos-VM SDK.  Pure-Python AES
  produces the right ciphertext length but the server rejects it (ret=9),
  meaning the Chaos VM uses a non-standard key schedule or wrapping that
  our reverse-engineering missed.  The browser always gets it right.

Why httpx for the HTTP call:
  Sending requests from inside the Playwright page (fetch/XHR) causes HTTP 500
  because the in-page context is missing the required auth/CSRF headers.
  httpx lets us set Origin, Referer, User-Agent, and all cookies explicitly.
"""
import asyncio
import json
import logging
from typing import Optional

import httpx

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_BASE    = "https://www.midasbuy.com"
_APPID   = "1900000047"
_PF      = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def _load_cookies(storage_state_path: str) -> dict:
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


async def _get_browser_envelope(
    payload: dict,
    storage_state_path: str,
    country_code: str,
) -> Optional[dict]:
    """Run Playwright to get {encrypt_msg, ctoken, ctoken_ver} via window.xMidas."""
    from accounts.services.playwright_crypto import get_browser_payload

    enc = await asyncio.to_thread(
        get_browser_payload, payload, storage_state_path, country_code
    )
    if not enc:
        logger.error("[SERVICE] failed to generate browser payload")
    return enc


async def _get(
    url: str,
    params: dict,
    cookies: dict,
    referer: str,
) -> Optional[dict]:
    headers = {
        "Accept":     "application/json, text/plain, */*",
        "Origin":     "https://www.midasbuy.com",
        "Referer":    referer,
        "User-Agent": _UA,
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(url, params=params, cookies=cookies, headers=headers)
        logger.info("[SERVICE] GET %s  status=%s", url, resp.status_code)
        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:400])
            return None
        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)
        return data
    except Exception:
        logger.exception("[SERVICE] GET request failed")
        return None


async def _post(
    url: str,
    body: dict,
    cookies: dict,
    referer: str,
) -> Optional[dict]:
    headers = {
        "Content-Type": "application/json",
        "Accept":       "application/json, text/plain, */*",
        "Origin":       "https://www.midasbuy.com",
        "Referer":      referer,
        "User-Agent":   _UA,
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.post(url, json=body, cookies=cookies, headers=headers)
        logger.info("[SERVICE] POST %s  status=%s", url, resp.status_code)
        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:400])
            return None
        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)
        return data
    except Exception:
        logger.exception("[SERVICE] POST request failed")
        return None


# ── Zone list (call first to discover PUBG Mobile server options) ─────────────

async def get_zone_list(
    storage_state_path: Optional[str] = None,
    country_code: str = "bd",
) -> list:
    """
    GET /interface/getAppSelectPf with {appid} → returns list of
    {zoneid, name, pf} objects the player can select as their server.
    """
    if not storage_state_path:
        return []

    payload = {"appid": _APPID}
    enc = await _get_browser_envelope(payload, storage_state_path, country_code)
    if not enc:
        return []

    session_cookies = _load_cookies(storage_state_path)
    if enc.get("ctoken"):
        session_cookies["ctoken"] = enc["ctoken"]

    referer = f"{_BASE}/midasbuy/{country_code}/redeem/pubgm"
    url     = _BASE + "/interface/getAppSelectPf"
    params  = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      enc["ctoken"],
        "ctoken_ver":  enc["ctoken_ver"],
    }

    data = await _get(url, params, session_cookies, referer)
    if not data or data.get("ret") != 0:
        logger.warning("[SERVICE] getAppSelectPf failed: %s", data)
        return []

    zones = (data.get("data") or {}).get("needSelectPF", {}).get("data", [])
    logger.info("[SERVICE] zones returned: %s", zones)
    return zones


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

    if not zone_id:
        return PlayerLookupResponse(
            success=False,
            error="zone_id is required. Call /api/zones first to get the server list.",
        )

    payload = {
        "openid":  player_id,
        "appid":   _APPID,
        "zone_id": zone_id,
    }

    enc = await _get_browser_envelope(payload, storage_state_path, country_code)
    if not enc:
        return PlayerLookupResponse(success=False, error="Failed to generate encrypted payload.")

    session_cookies = _load_cookies(storage_state_path)
    if enc.get("ctoken"):
        session_cookies["ctoken"] = enc["ctoken"]

    referer = f"{_BASE}/midasbuy/{country_code}/redeem/pubgm"
    url     = _BASE + "/interface/getCharacByOpenid"
    params  = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      enc["ctoken"],
        "ctoken_ver":  enc["ctoken_ver"],
    }

    logger.info("[SERVICE] GET %s  ctoken_prefix=%s  zone_id=%s", url, enc["ctoken"][:20], zone_id)
    data = await _get(url, params, session_cookies, referer)

    if data is None:
        return PlayerLookupResponse(success=False, error="API request failed. Check logs.")

    if data.get("ret") != 0:
        return PlayerLookupResponse(
            success=False,
            error=data.get("msg") or f"API error ret={data.get('ret')}",
        )

    role = data.get("data", {})
    return PlayerLookupResponse(
        success=True,
        player=PlayerInfo(
            player_id=player_id,
            username=role.get("charac_name") or role.get("roleName") or "",
            role_id=str(role.get("openid") or role.get("roleId") or player_id),
            server_id=str(role.get("pf") or ""),
            zone_id=str(role.get("zoneid") or zone_id),
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

    enc = await _get_browser_envelope(payload, storage_state_path, country_code)
    if not enc:
        return RedeemResponse(success=False, message="Failed to generate encrypted payload.")

    session_cookies = _load_cookies(storage_state_path)
    if enc.get("ctoken"):
        session_cookies["ctoken"] = enc["ctoken"]

    referer = f"{_BASE}/midasbuy/{country_code}/redeem/pubgm"
    url     = _BASE + "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo"
    body    = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      enc["ctoken"],
        "ctoken_ver":  enc["ctoken_ver"],
    }

    data = await _post(url, body, session_cookies, referer)

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

    enc = await _get_browser_envelope(payload, storage_state_path, country_code)
    if not enc:
        return RedeemResponse(success=False, message="Failed to generate encrypted payload.")

    session_cookies = _load_cookies(storage_state_path)
    if enc.get("ctoken"):
        session_cookies["ctoken"] = enc["ctoken"]

    referer = f"{_BASE}/midasbuy/{country_code}/redeem/pubgm"
    url     = _BASE + "/interface/shelfProto/shelves_svr/RedeemCode"
    body    = {
        "encrypt_msg": enc["encrypt_msg"],
        "ctoken":      enc["ctoken"],
        "ctoken_ver":  enc["ctoken_ver"],
    }

    data = await _post(url, body, session_cookies, referer)

    if data is None:
        return RedeemResponse(success=False, message="API request failed.")

    ret = data.get("ret", -1)
    msg = data.get("msg", "")
    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("Redeemed successfully!" if ret == 0 else "Redemption failed"),
        raw=data,
    )
