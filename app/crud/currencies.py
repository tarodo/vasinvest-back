from typing import List, Optional

from app.models import Currencies
from app.schemas import CurrencyDBIn, CurrencyIn


async def get_by_code(user_id: int, code: str) -> Optional[Currencies]:
    currency = await Currencies.filter(user_id=user_id, code=code).first()
    return currency


async def get_by_id(cur_id: int) -> Optional[Currencies]:
    currency = await Currencies.filter(id=cur_id).first()
    return currency


async def create(user_id: int, payload: CurrencyIn) -> Currencies:
    currency_in: CurrencyDBIn = CurrencyDBIn(user_id=user_id, **payload.dict())

    currencies: List[Currencies] = await Currencies.filter(user_id=user_id).all()
    for currency in currencies:
        currency.is_main = False
        await currency.save()

    currency: Currencies = Currencies(**currency_in.dict())
    await currency.save()

    return currency


async def update(currency: Currencies, payload: CurrencyIn) -> Currencies:
    await currency.update_from_dict(payload.dict())
    await currency.save()

    return currency


async def get_multi(skip: int, limit: int) -> List[Currencies]:
    return await Currencies().all().offset(skip).limit(limit).all()


async def get_multi_by_owner(user_id: int, skip: int, limit: int) -> List[Currencies]:
    return await Currencies().filter(user_id=user_id).offset(skip).limit(limit).all()


async def delete(currency: Currencies) -> Currencies:
    await currency.delete()
    return currency
