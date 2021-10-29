from enum import Enum

from fastapi import APIRouter, Depends

from app.api import raise_400
from app.api.deps import get_current_active_user
from app.crud.platforms import create, get_by_name
from app.models import Platforms, Users
from app.schemas import PlatformIn, PlatformOut

router = APIRouter()


class PlatformErrors(Enum):
    PlatformExists = "The platform with this name already exists"


@router.post("/", response_model=PlatformOut)
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
