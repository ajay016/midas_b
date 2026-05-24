"""
Business logic: player lookup and redeem code submission.

All Midasbuy API calls that pass through the xMidas interceptor send
{ encrypt_msg, ctoken_ver, ctoken } instead of the raw payload.
Endpoints that are GET requests pass those three fields as query parameters.
POST endpoints send them as the JSON body.

Confirmed from reverse-engineering of 46374.aa36b94c9a17d3c2.js lines 5573-5607.
"""

import httpx

from .constants import (
    DEFAULT_PF,
    ENDPOINT_QUERY_ROLE_DETAIL,
    ENDPOINT_SHELF_PROTO,
    MIDASBUY_BASE_URL,
    PUBGM_APPID,
    XMIDAS_TOKEN,
    XMIDAS_VERSION,
)
from .crypto import build_encrypted_payload
from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

# ── Shared HTTP headers (mirrors what the browser sends) ─────────────────────

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.midasbuy.com/",
    "Origin": "https://www.midasbuy.com",
    "Content-Type": "application/json",
}


# ── Player lookup ─────────────────────────────────────────────────────────────

async def get_player_info(player_id: str, country_code: str = "bd") -> PlayerLookupResponse:
    """
    Step 1 of the redeem flow: look up the player's username by UID.

    Endpoint: GET /interface/queryRoleDetail
    Observed params: player_id, appid, pf, country
    The xMidas interceptor wraps the params dict into { encrypt_msg, ctoken_ver, ctoken }.
    """
    raw_params = {
        "player_id": player_id,
        "appid": PUBGM_APPID,
        "pf": DEFAULT_PF,
        "country": country_code.upper(),
        "client_ver": "android",
    }

    envelope = build_encrypted_payload(raw_params, XMIDAS_TOKEN, XMIDAS_VERSION)

    url = MIDASBUY_BASE_URL + ENDPOINT_QUERY_ROLE_DETAIL

    async with httpx.AsyncClient(headers=_HEADERS, timeout=15) as client:
        resp = await client.get(url, params=envelope)

    if resp.status_code != 200:
        return PlayerLookupResponse(
            success=False,
            error=f"HTTP {resp.status_code}: {resp.text[:200]}",
        )

    data = resp.json()

    # Midasbuy returns ret=0 on success
    if data.get("ret") != 0:
        return PlayerLookupResponse(
            success=False,
            error=data.get("msg") or "Unknown error from API",
        )

    role = data.get("data", {})
    return PlayerLookupResponse(
        success=True,
        player=PlayerInfo(
            player_id=player_id,
            username=role.get("roleName") or role.get("role_name") or "",
            role_id=str(role.get("roleId") or role.get("role_id") or ""),
            server_id=str(role.get("serverId") or role.get("server_id") or ""),
            zone_id=str(role.get("zoneid") or ""),
        ),
    )


# ── Redeem code submission ────────────────────────────────────────────────────

async def submit_redeem_code(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
) -> RedeemResponse:
    """
    Step 2: submit the UC pin code for the given player.

    The redeem flow on midasbuy goes through the MIDAS shelf/checkout API.
    The raw payload is encrypted with xMidas before sending.

    NOTE: The exact endpoint and payload shape for pin-code redemption may
    require a live session token (openid / pf / sessionToken). Fill those
    in from your authenticated session if the API returns an auth error.
    """
    # Build the raw payload that would normally be sent to the server
    raw_payload = {
        "player_id": player_id,
        "appid": PUBGM_APPID,
        "pf": DEFAULT_PF,
        "country": country_code.upper(),
        "code": pin_code,                    # the UC pin / redeem code
        "channel": "os_midasbuy_redeem",     # confirmed channel name from 46374.js
        "client_ver": "android",
        "session_id": "hy_gameid",
        "session_type": "st_dummy",
    }

    envelope = build_encrypted_payload(raw_payload, XMIDAS_TOKEN, XMIDAS_VERSION)

    # The shelf/redeem endpoint accepts encrypted payloads as a POST body
    url = MIDASBUY_BASE_URL + ENDPOINT_SHELF_PROTO + "pubgm"

    async with httpx.AsyncClient(headers=_HEADERS, timeout=20) as client:
        resp = await client.post(url, json=envelope)

    raw = None
    try:
        raw = resp.json()
    except Exception:
        pass

    if resp.status_code != 200:
        return RedeemResponse(
            success=False,
            message=f"HTTP {resp.status_code}",
            raw=raw,
        )

    ret = (raw or {}).get("ret", -1)
    msg = (raw or {}).get("msg", "")

    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("OK" if ret == 0 else "Failed"),
        raw=raw,
    )
