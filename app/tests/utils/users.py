from typing import Dict, Optional

from fastapi.testclient import TestClient
from tortoise import Tortoise, run_async

from app.core.config import settings
from app.crud.users import create, get_by_email
from app.models import Users
from app.schemas import UserIn
from app.tests.utils.utils import random_email, random_lower_string

my_new_user: Optional[Users] = None


def get_testuser_token_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password, "scope": "me"}

    r = client.post("/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_user_in_db(db: str, email: str, password: str) -> None:
    global my_new_user
    await Tortoise.init(
        db_url=db,
        modules={"models": ["app.models.users"]},
    )

    user: Users = await get_by_email(email)
    if user:
        my_new_user = user

    new_user = UserIn(
        email=email, password=password, is_superuser=False, is_active=True
    )
    user = await create(new_user)
    my_new_user = user


def create_random_user() -> Users:
    run_async(
        create_user_in_db(
            settings.DATABASE_URL,
            random_email(),
            random_lower_string(),
        )
    )
    return my_new_user
