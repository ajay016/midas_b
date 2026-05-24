import httpx

from .crypto import build_encrypted_payload, get_xmidas_token
from .crypto.constants import (
    DEFAULT_PF, ENDPOINT_QUERY_ROLE_DETAIL, ENDPOINT_SHELF_PROTO,
    MIDASBUY_BASE_URL, PUBGM_APPID, XMIDAS_VERSION,
)
from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

_BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer":      "https://www.midasbuy.com/",
    "Origin":       "https://www.midasbuy.com",
    "Content-Type": "application/json",
}


def _make_headers(cookies: str | None) -> dict:
    h = dict(_BASE_HEADERS)
    if cookies:
        h["Cookie"] = cookies
    return h


async def get_player_info(
    player_id: str,
    country_code: str = "bd",
    cookies: str | None = None,
) -> PlayerLookupResponse:
    ctoken = await get_xmidas_token()
    raw = {
        "player_id":  player_id,
        "appid":      PUBGM_APPID,
        "pf":         DEFAULT_PF,
        "country":    country_code.upper(),
        "client_ver": "android",
    }
    envelope = build_encrypted_payload(raw, ctoken, XMIDAS_VERSION)
    url = MIDASBUY_BASE_URL + ENDPOINT_QUERY_ROLE_DETAIL

    async with httpx.AsyncClient(headers=_make_headers(cookies), timeout=15) as client:
        resp = await client.get(url, params=envelope)

    if resp.status_code != 200:
        return PlayerLookupResponse(success=False, error=f"HTTP {resp.status_code}")

    data = resp.json()
    if data.get("ret") != 0:
        return PlayerLookupResponse(success=False, error=data.get("msg") or "API error")

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


async def submit_redeem(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    cookies: str | None = None,
) -> RedeemResponse:
    ctoken = await get_xmidas_token()
    raw = {
        "player_id":    player_id,
        "appid":        PUBGM_APPID,
        "pf":           DEFAULT_PF,
        "country":      country_code.upper(),
        "code":         pin_code,
        "channel":      "os_midasbuy_redeem",
        "client_ver":   "android",
        "session_id":   "hy_gameid",
        "session_type": "st_dummy",
    }
    envelope = build_encrypted_payload(raw, ctoken, XMIDAS_VERSION)
    url = MIDASBUY_BASE_URL + ENDPOINT_SHELF_PROTO + "pubgm"

    async with httpx.AsyncClient(headers=_make_headers(cookies), timeout=20) as client:
        resp = await client.post(url, json=envelope)

    body = None
    try:
        body = resp.json()
    except Exception:
        pass

    if resp.status_code != 200:
        return RedeemResponse(success=False, message=f"HTTP {resp.status_code}", raw=body)

    ret = (body or {}).get("ret", -1)
    msg = (body or {}).get("msg", "")
    return RedeemResponse(
        success=(ret == 0),
        message=msg or ("Redeemed successfully" if ret == 0 else "Redemption failed"),
        raw=body,
    )
