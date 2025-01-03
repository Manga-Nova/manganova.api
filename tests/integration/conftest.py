from collections.abc import Generator
from os import environ
from typing import Any

import pytest
from fastapi.testclient import TestClient

from tests.integration.models import AuthResponse

environ["ENV"] = "test"
environ["DB_URL"] = "sqlite+aiosqlite:///test.db"


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    from src.__main__ import create_app

    with TestClient(create_app()) as client:
        yield client


@pytest.fixture(autouse=True)
def test_user(client: "TestClient") -> AuthResponse:
    response = client.post(
        "/auth/register",
        json={
            "username": "testClient",
            "password": "1234Abcd!@",
            "email": "testClient@gmail.com",
        },
    )
    return AuthResponse(**response.json())


@pytest.fixture(autouse=True)
def unlink_db() -> Generator[None, None]:
    from pathlib import Path

    yield

    Path("test.db").unlink(missing_ok=True)
