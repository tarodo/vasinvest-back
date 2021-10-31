from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud import platforms
from app.crud.tickers import (create, get_by_code, get_by_id, get_multi,
                              get_multi_by_owner, get_multi_by_platform,
                              is_mine, update)
from app.models import Platforms, Tickers, Users
from app.schemas import TickerIn, TickerOut

router = APIRouter()


class TickerErrors(Enum):
    TickerExists = "The ticker with this code already exists"
    NoRightsToCreate = "User doesn't have rights to create ticker in this platform"
    NoRightsToUpdate = "User doesn't have rights to update this ticker"
    NoRightsToRead = "User doesn't have rights to read this ticker"


@router.post("/", response_model=TickerOut, status_code=200)
async def create_ticker(
    payload: TickerIn, current_user: Users = Depends(get_current_active_user)
) -> Tickers:
    """
    Create new ticker.
    """
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


@router.put("/{ticker_id}", response_model=TickerOut, status_code=200)
async def update_ticker(
    payload: TickerIn,
    ticker_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Tickers:
    """
    Update ticker.
    """
    ticker: Tickers = await get_by_id(ticker_id)
    if not ticker:
        raise_400(TickerErrors.NoRightsToUpdate)

    if not current_user.is_superuser and not await is_mine(ticker, current_user):
        raise_400(TickerErrors.NoRightsToUpdate)

    new_platform: Platforms = await platforms.get_by_id(payload.platform_id)
    if not new_platform:
        raise_400(TickerErrors.NoRightsToCreate)

    if not current_user.is_superuser and not new_platform.user_id == current_user.id:
        raise_400(TickerErrors.NoRightsToCreate)

    await update(ticker, payload)
    return ticker


@router.get("/{ticker_id}", response_model=TickerOut, status_code=200)
async def get_ticker(
    ticker_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Tickers:
    """
    Retrieve ticker.
    """
    ticker: Tickers = await get_by_id(ticker_id)
    if not ticker:
        raise_400(TickerErrors.NoRightsToRead)

    if not current_user.is_superuser and not await is_mine(ticker, current_user):
        raise_400(TickerErrors.NoRightsToRead)

    return ticker


@router.get("/", response_model=List[TickerOut], status_code=200)
async def get_all_tickers(
    skip: int = 0,
    limit: int = 100,
    platform_id: Optional[int] = Query(None, gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> List[Tickers]:
    """
    Retrieve tickers.
    """
    if not platform_id:
        if current_user.is_superuser:
            tickers: List[Tickers] = await get_multi(skip, limit)
            return tickers
        else:
            return await get_multi_by_owner(current_user, skip, limit)
    else:
        platform: Platforms = await platforms.get_by_id(platform_id)
        if not platform:
            raise_400(TickerErrors.NoRightsToRead)

        if not current_user.is_superuser and not platform.user_id == current_user.id:
            raise_400(TickerErrors.NoRightsToRead)

        return await get_multi_by_platform(platform, skip, limit)
