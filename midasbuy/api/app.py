import logging
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "midasbuy_project.settings")
django.setup()

from asgiref.sync import sync_to_async
from fastapi import FastAPI, HTTPException, Query

from .schemas import PlayerLookupResponse, RedeemRequest, RedeemResponse
from .service import get_player_info, get_zone_list, submit_redeem

logger = logging.getLogger(__name__)
api_app = FastAPI(title="Midasbuy Redeem API", version="2.0.0")


def _resolve_session_sync(account_id: int) -> tuple[str | None, str | None]:
    """Sync helper — must be called via sync_to_async from async endpoints."""
    from accounts.models import MidasbuyAccount
    from django.conf import settings

    try:
        acct = MidasbuyAccount.objects.get(pk=account_id)
    except MidasbuyAccount.DoesNotExist:
        logger.warning("[API] account_id=%s not found", account_id)
        return None, None

    # Prefer the path stored by the login service; fall back to computed path
    ssp = acct.storage_state_path or os.path.join(
        acct.get_session_dir(str(settings.BASE_DIR)), "storage_state.json"
    )

    if not ssp or not os.path.exists(ssp):
        logger.warning(
            "[API] storage_state not found for account_id=%s ssp=%s", account_id, ssp
        )
        return None, None

    # Build cookie header — prefer in-DB cookie_data JSON, fall back to file
    cookie_header = ""
    if acct.cookie_data:
        cookie_header = "; ".join(
            f"{c['name']}={c['value']}"
            for c in acct.cookie_data
            if c.get("name") and c.get("value")
        )
    else:
        cookie_header = acct.get_cookie_header()

    logger.info(
        "[API] resolved session account_id=%s ssp=%s cookie_count=%s",
        account_id,
        ssp,
        len(acct.cookie_data) if acct.cookie_data else 0,
    )
    return ssp, cookie_header


async def _resolve_session(account_id: int | None) -> tuple[str | None, str | None]:
    if account_id is None:
        logger.warning("[API] no account_id provided")
        return None, None
    return await sync_to_async(_resolve_session_sync)(account_id)


@api_app.get("/zones")
async def zones(
    account_id:   int | None = Query(None),
    country_code: str = Query("bd"),
):
    """Return available PUBG Mobile server zones for getCharacByOpenid."""
    ssp, cookies = await _resolve_session(account_id)
    if not ssp:
        raise HTTPException(status_code=400, detail="No session. Please log in first.")
    zone_list = await get_zone_list(ssp, country_code)
    return {"zones": zone_list}


@api_app.get("/player-info", response_model=PlayerLookupResponse)
async def player_info(
    player_id:    str = Query(...),
    country_code: str = Query("bd"),
    zone_id:      str = Query(""),
    account_id:   int | None = Query(None),
):
    ssp, cookies = await _resolve_session(account_id)
    result = await get_player_info(player_id, country_code, ssp, cookies, zone_id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@api_app.post("/redeem", response_model=RedeemResponse)
async def redeem(body: RedeemRequest):
    ssp, cookies = await _resolve_session(body.account_id)
    return await submit_redeem(body.player_id, body.pin_code, body.country_code, ssp, cookies)
