from pydantic import BaseModel, EmailStr, constr
from typing import Optional
import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[constr(max_length=100)]
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True


class UserIn(UserBase):
    password: constr(min_length=8)


class UserOut(UserBase):
    created_at: datetime.datetime
    modified_at: datetime.datetime


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
