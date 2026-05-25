"""
Midasbuy API service.

All API calls use Python AES-256-CBC crypto (reverse-engineered from the
obfuscated window.xMidas SDK) to produce encrypt_msg.  The live xMidasToken
is captured once during login (saved to xmidas_token.txt) and reused here
as the AES key.  No Playwright is needed for individual API calls.

Encryption details (from midas_crypto/crypto.py):
  Key = first 32 bytes of hex-decoded xMidasToken
  IV  = 16 random bytes prepended to ciphertext
  Output = base64(IV + AES-256-CBC(payload_json))
"""
import base64
import json
import logging
import os
from typing import Optional

import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .schemas import PlayerInfo, PlayerLookupResponse, RedeemResponse

logger = logging.getLogger(__name__)

_BASE    = "https://www.midasbuy.com"
_APPID   = "1900000047"
_PF      = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"
_VERSION = "1.0.1"

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_HEADERS = {
    "User-Agent":   _UA,
    "Referer":      "https://www.midasbuy.com/",
    "Origin":       "https://www.midasbuy.com",
    "Content-Type": "application/json",
    "Accept":       "application/json, text/plain, */*",
}


# ── Crypto ────────────────────────────────────────────────────────────────────

def _xmidas_encrypt(payload: dict, ctoken_hex: str) -> str:
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    padded    = pad(plaintext, AES.block_size)
    iv        = os.urandom(16)
    key       = bytes.fromhex(ctoken_hex)[:32]
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(padded)).decode("ascii")


def _build_envelope(payload: dict, ctoken_hex: str) -> dict:
    return {
        "encrypt_msg": _xmidas_encrypt(payload, ctoken_hex),
        "ctoken_ver":  _VERSION,
        "ctoken":      ctoken_hex,
    }


# ── Session helpers ───────────────────────────────────────────────────────────

def _load_xmidas_token(storage_state_path: str) -> Optional[str]:
    """Read xMidasToken from xmidas_token.txt saved alongside storage_state."""
    session_dir = os.path.dirname(storage_state_path)
    token_path  = os.path.join(session_dir, "xmidas_token.txt")
    try:
        with open(token_path, encoding="utf-8") as f:
            token = f.read().strip()
        if token:
            logger.info("[SERVICE] xMidasToken loaded prefix=%s", token[:20])
            return token
        logger.error("[SERVICE] xmidas_token.txt is empty")
    except Exception as e:
        logger.error("[SERVICE] cannot read xmidas_token.txt: %s", e)
    return None


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


# ── API calls ─────────────────────────────────────────────────────────────────

async def get_player_info(
    player_id: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> PlayerLookupResponse:
    if not storage_state_path:
        return PlayerLookupResponse(success=False, error="No session. Please log in first.")

    ctoken = _load_xmidas_token(storage_state_path)
    if not ctoken:
        return PlayerLookupResponse(success=False, error="No xMidasToken found. Please re-login.")

    raw_params = {
        "player_id":  player_id,
        "appid":      _APPID,
        "pf":         _PF,
        "country":    country_code.upper(),
        "client_ver": "android",
    }

    envelope = _build_envelope(raw_params, ctoken)
    url      = _BASE + "/interface/queryRoleDetail"

    logger.info("[SERVICE] GET %s  ctoken_prefix=%s", url, ctoken[:20])

    try:
        async with httpx.AsyncClient(headers=_HEADERS, follow_redirects=True, timeout=15.0) as client:
            resp = await client.get(url, params=envelope)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:400])
            return PlayerLookupResponse(success=False, error=f"HTTP {resp.status_code}")

        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)

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
                username=role.get("roleName") or role.get("role_name") or role.get("charac_name") or "",
                role_id=str(role.get("roleId") or role.get("role_id") or role.get("openid") or player_id),
                server_id=str(role.get("serverId") or role.get("server_id") or ""),
                zone_id=str(role.get("zoneid") or ""),
            ),
        )

    except Exception:
        logger.exception("[SERVICE] get_player_info failed")
        return PlayerLookupResponse(success=False, error="Request failed. Check logs.")


async def query_code_info(
    player_id: str,
    pin_code: str,
    country_code: str = "bd",
    storage_state_path: Optional[str] = None,
    cookies: Optional[str] = None,
) -> RedeemResponse:
    if not storage_state_path:
        return RedeemResponse(success=False, message="No session.")

    ctoken       = _load_xmidas_token(storage_state_path)
    session_cookies = _load_cookies(storage_state_path)

    if not ctoken:
        return RedeemResponse(success=False, message="No xMidasToken. Please re-login.")

    raw_payload = {
        "roleId":  player_id,
        "appId":   _APPID,
        "game":    "pubgm",
        "pf":      _PF,
        "country": country_code.upper(),
        "code":    pin_code,
        "channel": "MIDASBUY_REDEEM",
    }

    envelope = _build_envelope(raw_payload, ctoken)
    url      = _BASE + "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo"

    logger.info("[SERVICE] POST %s  ctoken_prefix=%s", url, ctoken[:20])

    try:
        async with httpx.AsyncClient(
            headers=_HEADERS, cookies=session_cookies, follow_redirects=True, timeout=20.0
        ) as client:
            resp = await client.post(url, json=envelope)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:400])
            return RedeemResponse(success=False, message=f"HTTP {resp.status_code}")

        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)

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

    except Exception:
        logger.exception("[SERVICE] query_code_info failed")
        return RedeemResponse(success=False, message="Request failed. Check logs.")


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

    ctoken          = _load_xmidas_token(storage_state_path)
    session_cookies = _load_cookies(storage_state_path)

    raw_payload = {
        "roleId":    player_id,
        "appId":     _APPID,
        "game":      "pubgm",
        "pf":        _PF,
        "country":   country_code.upper(),
        "code":      pin_code,
        "channel":   "MIDASBUY_REDEEM",
        "channelId": "MIDASBUY_REDEEM",
    }

    envelope = _build_envelope(raw_payload, ctoken)
    url      = _BASE + "/interface/shelfProto/shelves_svr/RedeemCode"

    logger.info("[SERVICE] POST %s  ctoken_prefix=%s", url, ctoken[:20])

    try:
        async with httpx.AsyncClient(
            headers=_HEADERS, cookies=session_cookies, follow_redirects=True, timeout=20.0
        ) as client:
            resp = await client.post(url, json=envelope)

        logger.info("[SERVICE] status=%s", resp.status_code)

        if resp.status_code != 200:
            logger.error("[SERVICE] non-200: %s", resp.text[:400])
            return RedeemResponse(success=False, message=f"HTTP {resp.status_code}")

        data = resp.json()
        logger.info("[SERVICE] raw response: %s", data)

        ret = data.get("ret", -1)
        msg = data.get("msg", "")
        return RedeemResponse(
            success=(ret == 0),
            message=msg or ("Redeemed successfully!" if ret == 0 else "Redemption failed"),
            raw=data,
        )

    except Exception:
        logger.exception("[SERVICE] submit_redeem failed")
        return RedeemResponse(success=False, message="Request failed. Check logs.")
