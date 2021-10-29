from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.users import authenticate_user

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.Users = Depends(get_current_user)) -> models.Users:
    """
    Test access token
    """
    return current_user
