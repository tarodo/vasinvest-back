from typing import List, Optional

from app.models import Currencies, Users
from app.schemas import CurrencyIn, CurrencyOut, CurrencyDBIn


async def get_by_code(user_id: int, code: str) -> Optional[Currencies]:
    currency = await Currencies.filter(user_id=user_id, code=code).first()
    return currency


async def get_by_id(cur_id: int) -> Optional[Currencies]:
    currency = await Currencies.filter(id=cur_id).first()
    return currency


async def create(user: Users, payload: CurrencyIn) -> Currencies:
    currency_in: CurrencyDBIn = CurrencyDBIn(user_id=user.id, **payload.dict())
# TODO Add change for others status is_main to False
    currency: Currencies = Currencies(**currency_in.dict())
    await currency.save()

    return currency
