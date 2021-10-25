from fastapi import APIRouter, Depends
from passlib.handlers.bcrypt import bcrypt

from app.api.deps import get_current_active_user
from app.models.users import Users
from app.schemas.users import UserIn, UserOut

router = APIRouter()


@router.post('/', response_model=UserOut)
async def create_user(user: UserIn) -> Users:
    user_obj = Users(email=user.email, hashed_password=bcrypt.hash(user.password))
    await user_obj.save()
    return await user_obj


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    return current_user
