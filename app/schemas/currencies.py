import datetime
from typing import Optional

from pydantic import BaseModel, constr


class CurrencyBase(BaseModel):
    code: constr(max_length=10)
    name: Optional[constr(max_length=40)]
    is_main: Optional[bool] = False


class CurrencyIn(CurrencyBase):
    pass


class CurrencyOut(CurrencyBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime


class CurrencyDBBase(CurrencyBase):
    pass


class CurrencyDBIn(CurrencyDBBase):
    user_id: int
