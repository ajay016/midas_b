import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "midasbuy_project.settings")
django.setup()

from fastapi import FastAPI, HTTPException, Query, Request

from .schemas import PlayerLookupResponse, RedeemRequest, RedeemResponse
from .service import get_player_info, submit_redeem

api_app = FastAPI(title="Midasbuy Redeem API", version="2.0.0")


def _resolve_session(account_id: int | None) -> tuple[str | None, str | None]:
    """
    Returns (storage_state_path, cookie_header_string) for the given account,
    or (None, None) if no valid session exists.
    """
    if account_id is None:
        return None, None
    try:
        from accounts.models import MidasbuyAccount
        from django.conf import settings
        acct = MidasbuyAccount.objects.get(pk=account_id)
        sd = acct.get_session_dir(str(settings.BASE_DIR))
        ssp = os.path.join(sd, "storage_state.json")
        if not os.path.exists(ssp):
            return None, None
        return ssp, acct.get_cookie_header()
    except Exception:
        return None, None


@api_app.get("/player-info", response_model=PlayerLookupResponse)
async def player_info(
    player_id:    str = Query(...),
    country_code: str = Query("bd"),
    account_id:   int | None = Query(None),
):
    ssp, cookies = _resolve_session(account_id)
    result = await get_player_info(player_id, country_code, ssp, cookies)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@api_app.post("/redeem", response_model=RedeemResponse)
async def redeem(body: RedeemRequest):
    ssp, cookies = _resolve_session(body.account_id)
    return await submit_redeem(body.player_id, body.pin_code, body.country_code, ssp, cookies)
