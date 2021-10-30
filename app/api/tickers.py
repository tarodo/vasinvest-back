from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, Path

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud import platforms
from app.crud.tickers import get_by_code, create
from app.models import Users, Tickers, Platforms
from app.schemas import TickersOut, TickersIn

router = APIRouter()


class TickerErrors(Enum):
    TickerExists = "The ticker with this code already exists"
    NoRightsToCreate = "User doesn't have rights to create ticker in this platform"


@router.post("/", response_model=TickersOut, status_code=200)
async def create_platform(
    payload: TickersIn, current_user: Users = Depends(get_current_active_user)
) -> Tickers:
    """
    Create new ticker.
    """
    # TODO It doesn't work. FIX IT!
    platform: Platforms = await platforms.get_by_id(payload.platform_id)
    if not platform:
        raise_400(TickerErrors.NoRightsToCreate)

    if not current_user.is_superuser and not platform.user_id == current_user.id:
        raise_400(TickerErrors.NoRightsToCreate)

    ticker: Tickers = await get_by_code(platform, payload.code)
    if ticker:
        raise_400(TickerErrors.TickerExists)

    ticker = await create(payload)
    return ticker




