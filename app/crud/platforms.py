from typing import List, Optional

from app.models import Platforms, Users
from app.schemas import PlatformIn
from app.schemas.platforms import PlatformInDBBase


async def get_by_name(user_id: int, name: str) -> Optional[Platforms]:
    platform = await Platforms.filter(user_id=user_id, name=name).first()
    return platform


async def get_by_id(platform_id: int) -> Optional[Platforms]:
    platform = await Platforms.filter(id=platform_id).first()
    return platform


async def create(user: Users, payload: PlatformIn) -> Platforms:
    platform_in: PlatformInDBBase = PlatformInDBBase(user_id=user.id, **payload.dict())

    platform: Platforms = Platforms(**platform_in.dict())
    await platform.save()

    return platform


async def update(platform: Platforms, payload: PlatformIn) -> Platforms:
    await platform.update_from_dict(payload.dict())
    await platform.save()

    return platform


async def get_multi(skip: int, limit: int) -> List[Platforms]:
    return await Platforms().all().offset(skip).limit(limit).all()


async def get_multi_by_owner(user: Users, skip: int, limit: int) -> List[Platforms]:
    return await Platforms().filter(user_id=user.id).offset(skip).limit(limit).all()


async def delete(platform: Platforms) -> Platforms:
    await platform.delete()
    return platform
