from fastapi import FastAPI, HTTPException, Query, Request

from .schemas import PlayerLookupResponse, RedeemRequest, RedeemResponse
from .service import get_player_info, submit_redeem

api_app = FastAPI(title="Midasbuy Redeem API", version="1.0.0")


def _get_cookies(request: Request) -> str | None:
    return request.headers.get("X-Midasbuy-Cookie") or request.headers.get("Cookie") or None


@api_app.get("/player-info", response_model=PlayerLookupResponse)
async def player_info(
    request:      Request,
    player_id:    str = Query(..., description="PUBG Mobile player UID"),
    country_code: str = Query("bd", description="ISO country code"),
):
    result = await get_player_info(player_id, country_code, cookies=_get_cookies(request))
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@api_app.post("/redeem", response_model=RedeemResponse)
async def redeem(request: Request, body: RedeemRequest):
    return await submit_redeem(body.player_id, body.pin_code, body.country_code, cookies=_get_cookies(request))
