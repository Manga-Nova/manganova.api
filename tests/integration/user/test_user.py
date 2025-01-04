from typing import TYPE_CHECKING

import pytest

from tests.integration.models import AuthResponse

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


class TestUserSuite:
    _PATH = "/user"

    @pytest.fixture(autouse=True)
    def fixture_user(self, client: "TestClient") -> AuthResponse:
        return AuthResponse(
            **client.post(
                url="/auth/register",
                json={
                    "username": "fixtureUser",
                    "password": "1234Abcd!@",
                    "email": "fixtureUser@gmail.com",
                },
            ).json(),
        )

    def test_get_user(self, client: "TestClient", fixture_user: "AuthResponse") -> None:
        response = client.get(
            url=f"{self._PATH}/{fixture_user["user"]["id"]}",
        )

        assert response.status_code == 200
        assert response.json()["username"] == fixture_user["user"]["username"]
        assert response.json()["email"] == fixture_user["user"]["email"]

    def test_user_not_found(self, client: "TestClient") -> None:
        response = client.get(
            url=f"{self._PATH}/1234",
        )

        assert response.status_code == 404
        assert response.json()["className"] == "UserNotFoundError"
