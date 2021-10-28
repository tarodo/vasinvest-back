from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.users import get_testuser_token_headers
from main import app
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> Dict[str, str]:
    return get_testuser_token_headers(
        client=client, email=settings.TEST_USER_EMAIL, password=settings.TEST_USER_PASS
    )