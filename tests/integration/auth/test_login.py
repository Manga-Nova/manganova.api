from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


class TestAuthLoginSuite:
    _PATH = "/auth/login"

    @pytest.fixture(autouse=False)
    def fixture_user(self, client: "TestClient") -> None:
        client.post(
            url="/auth/register",
            json={
                "username": "fixtureUser",
                "password": "1234Abcd!@",
                "email": "fixtureUser@gmail.com",
            },
        )

    @pytest.mark.usefixtures("fixture_user")
    def test_login(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "password": "1234Abcd!@",
                "email": "fixtureUser@gmail.com",
            },
        )

        assert response.status_code == 200
        assert response.json()["user"]["username"] == "fixtureUser"
        assert response.json()["user"]["email"] == "fixtureUser@gmail.com"

    @pytest.mark.usefixtures("fixture_user")
    def test_email_error(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "password": "1234Abcd!@",
                "email": "fixtureTest@gmail.com",
            },
        )

        assert response.status_code == 401
        assert response.json()["className"] == "EmailOrPasswordError"

    @pytest.mark.usefixtures("fixture_user")
    def test_password_error(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "password": "1234Abcd!@Efg",
                "email": "fixtureUser@gmail.com",
            },
        )

        assert response.status_code == 401
        assert response.json()["className"] == "EmailOrPasswordError"
