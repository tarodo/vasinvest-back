from typing import List, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.models import Users
from app.schemas import UserIn


async def get_by_email(email: str) -> Optional[Users]:
    user = await Users.filter(email=email).first()
    if user:
        return user
    return None


async def authenticate_user(email: str, password: str) -> Union[Users, bool]:
    user = await get_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create(payload: UserIn) -> Users:
    user = Users(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_superuser=payload.is_superuser,
        is_active=payload.is_active,
    )

    await user.save()
    return user


async def get(user_id: int) -> Optional[Users]:
    user: Users = await Users.filter(id=user_id).first()
    return user


async def get_multi(skip: int, limit: int) -> List[Users]:
    return await Users().all().offset(skip).limit(limit).all()


async def update(user: Users, payload: UserIn) -> Users:
    data = payload.dict()
    if "password" in data:
        del data["password"]
    data["hashed_password"] = get_password_hash(payload.password)
    await user.update_from_dict(data)
    await user.save()

    return user
