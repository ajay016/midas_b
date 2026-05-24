"""
FastAPI application for the Midasbuy UC redeem helper.

Run with:
    uvicorn midas_crypto.fastapi_app:app --reload

Endpoints
---------
GET  /player-info?player_id=<uid>&country_code=bd
    Look up a PUBG Mobile player's username by UID.

POST /redeem
    Submit a UC pin code for a player.
    Body: { "player_id": "...", "pin_code": "...", "country_code": "bd" }

GET  /encrypt-demo
    Shows the raw encrypt_msg + ctoken for any payload (useful for testing).
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .constants import XMIDAS_TOKEN, XMIDAS_VERSION
from .crypto import build_encrypted_payload
from .schemas import (
    EncryptedEnvelope,
    PlayerLookupResponse,
    RedeemRequest,
    RedeemResponse,
)
from .service import get_player_info, submit_redeem_code

app = FastAPI(
    title="Midasbuy UC Redeem API",
    description="Generates xMidas encrypt_msg / ctoken and calls Midasbuy endpoints.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/player-info", response_model=PlayerLookupResponse)
async def player_info(
    player_id: str = Query(..., description="PUBG Mobile player UID"),
    country_code: str = Query("bd", description="ISO country code"),
):
    """
    Step 1: Enter the PUBG player ID → get username.

    Internally builds the encrypted payload and calls
    GET /interface/queryRoleDetail on midasbuy.com.
    """
    result = await get_player_info(player_id, country_code)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@app.post("/redeem", response_model=RedeemResponse)
async def redeem(body: RedeemRequest):
    """
    Step 2: Enter the UC pin code → redeem it for the player.

    Builds the AES-256-CBC encrypted payload (encrypt_msg + ctoken + ctoken_ver)
    and POSTs it to the Midasbuy shelf/redeem endpoint.
    """
    result = await submit_redeem_code(body.player_id, body.pin_code, body.country_code)
    return result


@app.get("/encrypt-demo", response_model=EncryptedEnvelope)
def encrypt_demo(payload_json: str = Query('{"player_id":"12345678"}')):
    """
    Debug endpoint: encrypts an arbitrary JSON payload and returns the
    { encrypt_msg, ctoken_ver, ctoken } envelope without sending it anywhere.
    """
    import json
    try:
        payload = json.loads(payload_json)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {exc}")

    return build_encrypted_payload(payload, XMIDAS_TOKEN, XMIDAS_VERSION)
