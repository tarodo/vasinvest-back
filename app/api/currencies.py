from enum import Enum

from fastapi import APIRouter, Depends

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud.currencies import get_by_code, get_by_id, create
from app.models import Currencies, Users
from app.schemas import CurrencyIn, CurrencyOut

router = APIRouter()


class CurrencyErrors(Enum):
    CurrencyExists = "The currency with this code already exists"


@router.post("/", response_model=CurrencyOut, status_code=200)
async def create_currency(
    payload: CurrencyIn, current_user: Users = Depends(get_current_active_user)
) -> Currencies:
    """
    Create new currency.
    """
    currency: Currencies = await get_by_code(current_user.id, payload.code)
    if currency:
        raise_400(CurrencyErrors.CurrencyExists)

    currency: Currencies = await create(current_user, payload)
    return currency
