"""
Python port of window.xMidas() — AES-256-CBC encryption.

Key   : first 32 bytes of hex-decoded xMidasToken (ctoken)
IV    : 16 random bytes, prepended to the ciphertext
Output: Base64(IV + AES-256-CBC(PKCS7(JSON(payload))))

publicParams mirrors the ei() function from 91.79b63beb.bundle.js module 36453.
They are captured once during login (page_data.json) and merged into every payload.
"""
import base64
import json
import os
import random
from typing import Optional

import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

_PF = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"


def xmidas_encrypt(payload: dict, ctoken_hex: str) -> str:
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    padded    = pad(plaintext, AES.block_size)
    iv        = os.urandom(16)
    key       = bytes.fromhex(ctoken_hex)[:32]
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(padded)).decode("ascii")


def build_encrypted_payload(payload: dict, ctoken_hex: str, ctoken_ver: str) -> dict:
    return {
        "encrypt_msg": xmidas_encrypt(payload, ctoken_hex),
        "ctoken_ver":  ctoken_ver,
        "ctoken":      ctoken_hex,
    }


def build_public_params(page_data: dict, country_code: str = "bd") -> dict:
    """Build the publicParams dict that mirrors ei() in the Midasbuy SPA bundle."""
    device_id = page_data.get("midasbuyDeviceId", "")
    muid      = page_data.get("midasuid", "")
    tdrc_fp   = page_data.get("uuidCookie", "")

    cgi_extend_obj = json.dumps(
        {"device_id": device_id, "pagetoken": "", "tdrc_fp": tdrc_fp, "muid": muid},
        separators=(",", ":"),
    )
    cgi_extend = base64.b64encode(cgi_extend_obj.encode()).decode()
    drm_info   = base64.b64encode(b"{}").decode()

    return {
        "appid":         page_data.get("appid", "1900000047"),
        "pf":            _PF,
        "zoneid":        page_data.get("zoneid", "1"),
        "country":       (page_data.get("country") or country_code or "bd").upper(),
        "device_id":     device_id,
        "pagetoken":     "",
        "tdrc_fp":       tdrc_fp,
        "muid":          muid,
        "cgi_extend":    cgi_extend,
        "drm_info":      drm_info,
        "midasbuyArea":  page_data.get("midasbuyArea", ""),
        "shopcode":      "",
        "buyType":       "",
        "midas_sdk":     "1",
        "currency_type": page_data.get("currency_type", "USD"),
        "_id":           random.random(),
        "sc":            "",
        "from":          "",
        "task_token":    "",
    }


def call_api_python(
    payload: dict,
    endpoint: str,
    storage_state_path: str,
    country_code: str = "bd",
    xmidas_token: str = "",
    page_data: Optional[dict] = None,
) -> Optional[dict]:
    """
    Encrypt the full merged payload in Python and POST to Midasbuy via httpx.

    This is faster and more reliable than the browser-based approach because
    it avoids the window.xMidas availability race condition entirely.
    """
    if not xmidas_token:
        return None

    public_params = build_public_params(page_data or {}, country_code)
    full_payload  = {**public_params, **payload}  # payload wins on overlap

    body = build_encrypted_payload(full_payload, xmidas_token, "1.0.1")

    # Extract cookies that apply to www.midasbuy.com
    with open(storage_state_path, encoding="utf-8") as f:
        ss = json.load(f)

    cookies = {}
    for c in ss.get("cookies", []):
        name  = c.get("name", "")
        value = c.get("value", "")
        if not name or not value:
            continue
        domain = c.get("domain", "")
        if "midasbuy.com" in domain:
            cookies[name] = value

    url = f"https://www.midasbuy.com{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept":       "application/json, text/plain, */*",
        "User-Agent":   (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Origin":       "https://www.midasbuy.com",
        "Referer":      f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm",
    }

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        resp = client.post(url, json=body, headers=headers, cookies=cookies)
        resp.raise_for_status()
        return resp.json()
