from typing import List, Optional

from app.models import Platforms, Tickers, Users
from app.schemas import TickerIn


async def get_by_code(platform: Platforms, code: str) -> Optional[Tickers]:
    ticker = await Tickers.filter(platform_id=platform.id, code=code).first()
    return ticker


async def get_by_id(ticker_id: int) -> Optional[Tickers]:
    ticker = await Tickers.filter(id=ticker_id).first()
    return ticker


async def is_mine(ticker: Tickers, user: Users) -> bool:
    platform: Platforms = await ticker.platform
    if user.id == platform.user_id:
        return True

    return False


async def create(payload: TickerIn) -> Tickers:
    ticker: Tickers = Tickers(**payload.dict())
    await ticker.save()

    return ticker


async def update(ticker: Tickers, payload: TickerIn) -> Tickers:
    await ticker.update_from_dict(payload.dict())
    await ticker.save()

    return ticker


async def get_multi(skip: int, limit: int) -> List[Tickers]:
    return await Tickers().all().offset(skip).limit(limit).all()


async def get_multi_by_owner(user: Users, skip: int, limit: int) -> List[Tickers]:
    platforms: List[Platforms] = await user.platforms
    tickers = []
    for platform in platforms:
        plat_tickers: List[Tickers] = await platform.tickers
        if plat_tickers:
            tickers += plat_tickers
    return tickers[skip : skip + limit]


async def get_multi_by_platform(
    platform: Platforms, skip: int, limit: int
) -> List[Tickers]:
    tickers: List[Tickers] = await platform.tickers
    return tickers[skip : skip + limit]
