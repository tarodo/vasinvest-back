import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from main import app
from app.tests.utils.utils import random_email, random_lower_string


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
