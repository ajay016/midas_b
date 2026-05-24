"""
Fetches the live xMidasToken from the Midasbuy CDN at runtime.

The token is embedded in xmidas-sdk.js as:
    xMidasTokenInput.value = "3ba22cbf...";
It can rotate between SDK deployments, so we never hardcode it.
"""
import re
import httpx

# The xmidas-sdk.js URL is referenced in the redeem page HTML.
# It loads from the same CDN and injects the token into the DOM.
_SDK_URL = (
    "https://cdn.midasbuy.com/js/x-midas/"
    "kEc9hjFh5DQJbz_iPEWrfFxadMVk4PbLDS-5P8jE73pfdUuDwNGKNVZjdEztcHdofAVaHXo6zRGXgLwuvsK_afAEj6w_mKyiUmq-7AesIRU~.js"
)

_FALLBACK_TOKEN = (
    "3ba22cbf8bea411868a1ea9611979910684f8fc4f493a76eb5129303e93a941f"
    "197616e264eab6c363f09d9be3624bd2"
)

_cached_token: str | None = None


async def get_xmidas_token() -> str:
    global _cached_token
    if _cached_token:
        return _cached_token

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(_SDK_URL)
        match = re.search(r'xMidasTokenInput\.value\s*=\s*"([a-f0-9]{90,})"', resp.text)
        if match:
            _cached_token = match.group(1)
            return _cached_token
    except Exception:
        pass

    # Fall back to the token from our reverse-engineering session
    _cached_token = _FALLBACK_TOKEN
    return _cached_token
