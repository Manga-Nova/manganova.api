from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


class TestAuthRegisterSuite:
    _PATH = "/auth/register"

    @pytest.fixture
    def fixture_user(self, client: "TestClient") -> None:
        client.post(
            url=self._PATH,
            json={
                "username": "fixtureUser",
                "password": "1234Abcd!@",
                "email": "fixtureUser@gmail.com",
            },
        )

    def test_register(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "testRegister",
                "password": "1234Abcd!@",
                "email": "testRegister@gmail.com",
            },
        )

        assert response.status_code == 201
        assert response.json()["user"]["username"] == "testRegister"
        assert response.json()["user"]["email"] == "testRegister@gmail.com"

    @pytest.mark.usefixtures("fixture_user")
    def test_register_username_conflict(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "fixtureUser",
                "password": "1234Abcd!@",
                "email": "registerUser@gmail.com",
            },
        )

        assert response.status_code == 409
        assert response.json()["className"] == "UsernameAlreadyExistsError"

    @pytest.mark.usefixtures("fixture_user")
    def test_register_email_conflict(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "newFixtureUser",
                "password": "1234Abcd!@",
                "email": "fixtureUser@gmail.com",
            },
        )

        assert response.status_code == 401
        assert response.json()["className"] == "EmailOrPasswordError"

    @pytest.mark.usefixtures("fixture_user")
    def test_register_email_regex_error(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "newFixtureUser",
                "password": "1234Abcd!@",
                "email": "a@some_random_email.online",
            },
        )

        assert response.status_code == 400
        assert response.json()["className"] == "InvalidEmailError"

    @pytest.mark.usefixtures("fixture_user")
    def test_register_password_regex_error(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "testRegister",
                "password": "abcd1234",
                "email": "testRegister@gmail.com",
            },
        )

        assert response.status_code == 400
        assert response.json()["className"] == "InvalidPasswordError"

    @pytest.mark.usefixtures("fixture_user")
    def test_register_username_regex_error(self, client: "TestClient") -> None:
        response = client.post(
            url=self._PATH,
            json={
                "username": "My-Username",
                "password": "1234Abcd!@",
                "email": "testRegister@gmail.com",
            },
        )

        assert response.status_code == 400
        assert response.json()["className"] == "InvalidUsernameError"
