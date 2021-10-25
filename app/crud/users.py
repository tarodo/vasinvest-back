from typing import Optional, Union
from decouple import config

from app.models.users import Users

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


async def get_user_by_email(email: str) -> Optional[Users]:
    user = await Users.filter(email=email).first()
    if user:
        return user
    return None


async def authenticate_user(email: str, password: str) -> Union[Users, bool]:
    user = await get_user_by_email(email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

