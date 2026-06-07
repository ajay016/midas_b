from pydantic import BaseModel, Field


class PlayerLookupRequest(BaseModel):
    player_id:    str = Field(..., description="PUBG Mobile player UID")
    country_code: str = Field("bd", description="ISO country code")


class RedeemRequest(BaseModel):
    player_id:    str = Field(..., description="PUBG Mobile player UID")
    pin_code:     str = Field(..., description="UC redeem pin code")
    country_code: str = Field("bd", description="ISO country code")
    zone_id:      str = Field("1", description="Player zone ID returned by lookup")
    account_id:   int | None = Field(None, description="MidasbuyAccount ID to use")
    rc_token:     str | None = Field(None, description="Risk-control verification token")
    rc_uuid:      str | None = Field(None, description="Risk-control verification UUID")


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
    success:               bool
    message:               str
    verification_required: bool = False
    challenge_url:         str | None = None
    risk_sdk_url:          str | None = None
    raw:                   dict | None = None
