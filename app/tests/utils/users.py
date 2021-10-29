from typing import Dict

from fastapi.testclient import TestClient


def get_testuser_token_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password, "scope": "me"}

    r = client.post("/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
