from collections.abc import Generator
from datetime import datetime
from os import environ
from typing import Any, TypedDict

import pytest
from fastapi.testclient import TestClient

environ["ENV"] = "test"
environ["DB_URL"] = "sqlite+aiosqlite:///test.db"


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    from src.__main__ import create_app

    with TestClient(create_app()) as client:
        yield client


class _TestUser(TypedDict):
    id: int
    created_at: datetime
    username: str
    email: str


class _TestUserResponse(TypedDict):
    access_token: str
    user: _TestUser


@pytest.fixture(autouse=True)
def test_user(client: "TestClient") -> _TestUserResponse:
    response = client.post(
        "/auth/register",
        json={
            "username": "testClient",
            "password": "1234Abcd!@",
            "email": "testClient@gmail.com",
        },
    )
    return _TestUserResponse(**response.json())


@pytest.fixture(autouse=True)
def unlink_db() -> Generator[None, None]:
    from pathlib import Path

    yield

    Path("test.db").unlink(missing_ok=True)
