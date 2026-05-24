"""
Python port of window.xMidas() — AES-256-CBC encryption.

Key   : first 32 bytes of hex-decoded XMIDAS_TOKEN
IV    : 16 random bytes, prepended to the ciphertext
Output: Base64(IV + AES-256-CBC(PKCS7(JSON(payload))))
"""
import base64
import json
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


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
