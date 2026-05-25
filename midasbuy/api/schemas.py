from pydantic import BaseModel, Field


class PlayerLookupRequest(BaseModel):
    player_id:    str = Field(..., description="PUBG Mobile player UID")
    country_code: str = Field("bd", description="ISO country code")
    zone_id:      str = Field("", description="PUBG Mobile server zone ID (from /api/zones)")


class RedeemRequest(BaseModel):
    player_id:    str = Field(..., description="PUBG Mobile player UID")
    pin_code:     str = Field(..., description="UC redeem pin code")
    country_code: str = Field("bd", description="ISO country code")
    account_id:   int | None = Field(None, description="MidasbuyAccount ID to use")


class PlayerInfo(BaseModel):
    player_id:  str
    username:   str
    role_id:    str = ""
    server_id:  str = ""
    zone_id:    str = ""


class PlayerLookupResponse(BaseModel):
    success: bool
    player:  PlayerInfo | None = None
    error:   str | None = None


class RedeemResponse(BaseModel):
    success: bool
    message: str
    raw:     dict | None = None
