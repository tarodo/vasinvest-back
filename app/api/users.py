from datetime import timedelta, datetime
from typing import List, Optional

import jwt
from decouple import config
from passlib.context import CryptContext

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.bcrypt import bcrypt

from app.crud.users import authenticate_user, get_current_user
from app.models.users import Users
from app.schemas.token import Token
from app.schemas.users import UserIn, UserOut

ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/users/', response_model=UserOut)
async def create_user(user: UserIn) -> Users:
    user_obj = Users(email=user.email, hashed_password=bcrypt.hash(user.password))
    await user_obj.save()
    return await user_obj


@router.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
