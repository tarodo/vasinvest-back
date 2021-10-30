from typing import Optional

from app.models import Users, Tickers, Platforms
from app.schemas import TickersIn


async def get_by_code(platform: Platforms, code: str) -> Optional[Tickers]:
    ticker = await Tickers.filter(platform_id=platform.id, code=code).first()
    return ticker


async def create(payload: TickersIn) -> Tickers:
    ticker: Tickers = Tickers(**payload.dict())
    await ticker.save()

    return ticker