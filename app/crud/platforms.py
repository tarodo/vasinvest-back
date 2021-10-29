from typing import Optional

from app.models import Platforms, Users
from app.schemas import PlatformIn
from app.schemas.platforms import PlatformInDBBase


async def get_by_name(user_id: int, name: str) -> Optional[Platforms]:
    platform = await Platforms.filter(user_id=user_id, name=name).first()
    return platform


async def create(user: Users, payload: PlatformIn) -> Platforms:
    platform_in: PlatformInDBBase = PlatformInDBBase(user_id=user.id, **payload.dict())

    platform: Platforms = Platforms(**platform_in.dict())
    await platform.save()

    return platform
