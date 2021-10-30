from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, Path

from app.api import raise_400
from app.api.deps import get_current_active_superuser, get_current_active_user
from app.crud.users import create, get, get_by_email, get_multi, update
from app.models.users import Users
from app.schemas import UserIn, UserOut

router = APIRouter()


class UserErrors(Enum):
    UserExists = "The user with this email already exists"
    UserNotExists = "The user with this email doesn't exist"
    UserNotSU = "User is not a superuser"


@router.post("/", response_model=UserOut)
async def create_user(
    payload: UserIn, current_user: Users = Depends(get_current_active_superuser)
) -> Users:
    """
    Create new user.
    """
    user = await get_by_email(payload.email)
    if user:
        raise_400(UserErrors.UserExists)

    user_in = await create(payload)
    return user_in


@router.get("/me", response_model=UserOut, status_code=200)
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    """
    Get user info.
    """
    return current_user


@router.get("/", response_model=List[UserOut], status_code=200)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Users = Depends(get_current_active_superuser),
) -> List[Users]:
    """
    Get all users info.
    """
    return await get_multi(skip, limit)


@router.put("/me", response_model=UserOut, status_code=200)
async def update_me(
    payload: UserIn, current_user: Users = Depends(get_current_active_user)
):
    """
    Update me.
    """
    if not current_user.is_superuser:
        if payload.is_superuser:
            raise_400(UserErrors.UserNotSU)

    payload.is_active = True

    user = await update(current_user, payload)
    return user


@router.put("/{user_id}", response_model=UserOut, status_code=200)
async def update_user(
    payload: UserIn,
    user_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_superuser),
):
    """
    Update any user.
    """
    user = await get(user_id)
    if not user:
        raise_400(UserErrors.UserNotExists)

    user = await update(user, payload)
    return user
