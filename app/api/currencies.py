from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, Path

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud.currencies import (create, delete, get_by_code, get_by_id,
                                 get_multi, get_multi_by_owner, update)
from app.models import Currencies, Users
from app.schemas import CurrencyIn, CurrencyOut

router = APIRouter()


class CurrencyErrors(Enum):
    CurrencyExists = "The currency with this code already exists"
    CurrencyNotExists = "The currency with this code isn't exist"
    NoRightsToUpdate = "User doesn't have rules to update this currency"
    NoRightsToRead = "User doesn't have rules to read this currency"
    NoRightsToDelete = "User doesn't have rules to delete this currency"


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

    currency: Currencies = await create(current_user.id, payload)
    return currency


@router.put("/{currency_id}", response_model=CurrencyOut, status_code=200)
async def update_currency(
    payload: CurrencyIn,
    currency_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Currencies:
    """
    Update currency.
    """
    currency = await get_by_id(currency_id)
    if not currency:
        if current_user.is_superuser:
            raise_400(CurrencyErrors.CurrencyNotExists)
            # TODO Implement this handler everywhere
        else:
            raise_400(CurrencyErrors.NoRightsToUpdate)
    if not current_user.is_superuser:
        if currency.user_id != current_user.id:
            raise_400(CurrencyErrors.NoRightsToUpdate)

    currency = await update(currency, payload)
    return currency


@router.get("/{currency_id}", response_model=CurrencyOut, status_code=200)
async def get_currency(
    currency_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Currencies:
    """
    Retrieve currency
    """
    currency: Currencies = await get_by_id(currency_id)
    if not currency:
        if current_user.is_superuser:
            raise_400(CurrencyErrors.CurrencyNotExists)
        else:
            raise_400(CurrencyErrors.NoRightsToRead)

    if not current_user.is_superuser:
        if currency.user_id != current_user.id:
            raise_400(CurrencyErrors.NoRightsToRead)

    return currency


@router.get("/", response_model=List[CurrencyOut], status_code=200)
async def get_all_currencies(
    skip: int = 0,
    limit: int = 100,
    current_user: Users = Depends(get_current_active_user),
) -> List[Currencies]:
    """
    Retrieve currencies.
    If you are an admin you will get all currencies.
    If not you will get just yours.
    """

    if current_user.is_superuser:
        currencies: List[Currencies] = await get_multi(skip, limit)
        return currencies
    else:
        return await get_multi_by_owner(current_user.id, skip, limit)


@router.delete("/{currency_id}", response_model=CurrencyOut, status_code=200)
async def delete_currency(
    currency_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Currencies:
    """
    Delete currency
    """
    currency: Currencies = await get_by_id(currency_id)
    if not currency:
        if current_user.is_superuser:
            raise_400(CurrencyErrors.CurrencyNotExists)
        else:
            raise_400(CurrencyErrors.NoRightsToDelete)

    if not current_user.is_superuser:
        if currency.user_id != current_user.id:
            raise_400(CurrencyErrors.NoRightsToDelete)

    await delete(currency)
    return currency
