import datetime
from typing import Optional

from pydantic import BaseModel, constr


class PlatformBase(BaseModel):
    name: Optional[constr(max_length=100)]
    description: Optional[constr(max_length=1000)]
    is_active: Optional[bool] = True


class PlatformIn(PlatformBase):
    pass


class PlatformOut(PlatformBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class PlatformInDBBase(PlatformBase):
    user_id: int
