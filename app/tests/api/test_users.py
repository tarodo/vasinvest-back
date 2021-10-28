from typing import Dict

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import Users
from app.schemas import UserOut, UserIn
from main import app
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get("/users/me", headers=superuser_token_headers)

    assert r.status_code == 200

    current_user: UserOut = UserOut(**r.json())
    assert current_user
    assert current_user.is_active
    assert current_user.is_superuser
    assert current_user.email == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get("/users/me", headers=normal_user_token_headers)

    assert r.status_code == 200

    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_create_user(
        client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    payload = {
        'email': random_email(),
        'password': random_lower_string()
    }
    r = client.post('/users/', headers=superuser_token_headers, json=payload)
    assert r.status_code == 200

    new_user: UserOut = UserOut(**r.json())
    assert new_user
    assert new_user.email == payload['email']


def test_create_user_again(
        client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    payload = {
        'email': settings.TEST_USER_EMAIL,
        'password': random_lower_string()
    }
    r = client.post('/users/', headers=superuser_token_headers, json=payload)
    assert r.status_code == 400
