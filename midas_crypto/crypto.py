"""
Python port of window.xMidas() from kEc9hjFh5DQJbz...js

Reverse-engineered from the Tencent Chaos VM (28,796-word bytecode):
  - Algorithm : AES-256-CBC
  - Key        : first 32 bytes of the hex-decoded xMidasToken
  - IV         : 16 cryptographically random bytes (prepended to output)
  - Padding    : PKCS7 (16-byte block size)
  - Input      : JSON.stringify(payload)  →  UTF-8 bytes
  - Output     : Base64( IV || ciphertext )

The caller in 46374.aa36b94c9a17d3c2.js (lines 5597-5605) then wraps this as:
    { encrypt_msg: <result>, ctoken_ver: "1.0.1", ctoken: <raw_token_hex> }
"""

import base64
import json
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def _derive_key(ctoken_hex: str) -> bytes:
    """
    AES-256 key = first 32 bytes of hex-decoded ctoken.
    The xMidas VM selects AES-256 when keylen >= 25 bytes;
    the 48-byte token always satisfies this threshold.
    """
    return bytes.fromhex(ctoken_hex)[:32]


def xmidas_encrypt(payload: dict, ctoken_hex: str) -> str:
    """
    Encrypts `payload` exactly as window.xMidas({d: JSON.stringify(payload)}).

    Returns the base64-encoded string that becomes encrypt_msg.
    """
    # Step 1 – serialize (mirrors JSON.stringify in the JS caller)
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    # Step 2 – PKCS7 pad to AES block size
    padded = pad(plaintext, AES.block_size)

    # Step 3 – random 16-byte IV (Math.random() loop in the VM)
    iv = os.urandom(16)

    # Step 4 – AES-256-CBC encrypt
    key = _derive_key(ctoken_hex)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)

    # Step 5 – prepend IV and base64-encode
    # (the caller does: btoa(String.fromCharCode(...hexString.match(/../g).map(parseInt(e,16)))))
    return base64.b64encode(iv + ciphertext).decode("ascii")


def build_encrypted_payload(payload: dict, ctoken_hex: str, ctoken_ver: str) -> dict:
    """
    Returns the full encrypted envelope that replaces the raw payload in any
    Midasbuy API request that goes through the xMidas interceptor.

    Mirrors the return value of function i(e) in 46374.aa36b94c9a17d3c2.js:
        { encrypt_msg, ctoken_ver, ctoken }
    """
    return {
        "encrypt_msg": xmidas_encrypt(payload, ctoken_hex),
        "ctoken_ver": ctoken_ver,
        "ctoken": ctoken_hex,
    }
