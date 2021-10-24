from typing import Optional, Union

import jwt
from decouple import config
from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from pydantic import ValidationError
from starlette import status

from app.models.users import Users
from app.schemas.token import TokenData

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


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


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=email)
    except (jwt.DecodeError, ValidationError):
        raise credentials_exception

    user = await get_user_by_email(email)
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
