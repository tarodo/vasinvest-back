from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_wrong(client: TestClient) -> None:
    login_data = {
        "username": "wrong@wrong.com",
        "password": "wrong_pass",
    }
    r = client.post("/token", data=login_data)
    assert r.status_code == 401


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        "/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
