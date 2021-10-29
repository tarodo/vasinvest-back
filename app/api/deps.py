from enum import Enum

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from starlette import status

from app.api import raise_400
from app.core.config import settings
from app.crud.users import get_by_email
from app.models.users import Users
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user."},
)


class LoginErrors(Enum):
    NotActive = "Inactive user"
    NotSU = "Not superuser"


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> Users:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=email)
    except (jwt.DecodeError, ValidationError):
        raise credentials_exception

    user = await get_by_email(email)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Users = Security(get_current_user, scopes=["me"])
) -> Users:
    if not current_user.is_active:
        raise_400(LoginErrors.NotActive)
    return current_user


async def get_current_active_superuser(
    current_user: Users = Security(get_current_user, scopes=["me"])
) -> Users:
    if not current_user.is_superuser:
        raise_400(LoginErrors.NotSU)
    return current_user
