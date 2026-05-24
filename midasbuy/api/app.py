from fastapi import FastAPI, HTTPException, Query

from .schemas import PlayerLookupResponse, RedeemRequest, RedeemResponse
from .service import get_player_info, submit_redeem

api_app = FastAPI(title="Midasbuy Redeem API", version="1.0.0")


@api_app.get("/player-info", response_model=PlayerLookupResponse)
async def player_info(
    player_id:    str = Query(..., description="PUBG Mobile player UID"),
    country_code: str = Query("bd", description="ISO country code"),
):
    result = await get_player_info(player_id, country_code)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@api_app.post("/redeem", response_model=RedeemResponse)
async def redeem(body: RedeemRequest):
    return await submit_redeem(body.player_id, body.pin_code, body.country_code)
