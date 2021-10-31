import datetime
from typing import Optional

from pydantic import BaseModel, constr

from app.models.tickers import TickerTypesEnum


class TickersBase(BaseModel):
    platform_id: int
    code: constr(max_length=20)
    name: Optional[constr(max_length=100)]
    description: Optional[constr(max_length=1000)]
    type: TickerTypesEnum


class TickerIn(TickersBase):
    pass


class TickerOut(TickersBase):
    id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime
