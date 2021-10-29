from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, Path

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud.platforms import (create, get_by_id, get_by_name, get_multi,
                                get_multi_by_owner, update)
from app.models import Platforms, Users
from app.schemas import PlatformIn, PlatformOut

router = APIRouter()


class PlatformErrors(Enum):
    PlatformExists = "The platform with this name already exists"
    NoRightsToUpdate = "User doesn't have rules to update this platform"


@router.post("/", response_model=PlatformOut, status_code=200)
async def create_platform(
    payload: PlatformIn, current_user: Users = Depends(get_current_active_user)
) -> Platforms:
    """
    Create new platform.
    """
    platform: Platforms = await get_by_name(current_user.id, payload.name)
    if platform:
        raise_400(PlatformErrors.PlatformExists)

    platform: Platforms = await create(current_user, payload)
    return platform


@router.put("/{platform_id}", response_model=PlatformOut, status_code=200)
async def update_platform(
    payload: PlatformIn,
    platform_id: int = Path(..., gt=0),
    current_user: Users = Depends(get_current_active_user),
) -> Platforms:
    """
    Update platform.
    """
    platform: Platforms = await get_by_id(platform_id)
    if not platform:
        raise_400(PlatformErrors.NoRightsToUpdate)
    if not current_user.is_superuser:
        if platform.user_id != current_user.id:
            raise_400(PlatformErrors.NoRightsToUpdate)

    platform = await update(platform, payload)
    return platform


@router.get("/", response_model=List[PlatformOut], status_code=200)
async def get_all_platforms(
    skip: int = 0,
    limit: int = 100,
    current_user: Users = Depends(get_current_active_user),
) -> List[Platforms]:
    """
    Retrieve platforms.
    """
    if current_user.is_superuser:
        platforms = await get_multi(skip, limit)
        print(platforms)
        return platforms
    else:
        return await get_multi_by_owner(current_user, skip, limit)

# TODO Write endpont to get one and delete one
