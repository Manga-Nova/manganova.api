from typing import TYPE_CHECKING

import pytest

from tests.integration.models import AuthResponse

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from httpx import Response


class TestAuthChangePasswordSuite:
    _PATH = "/auth/change-password"

    @pytest.fixture(autouse=True)
    def fixture_user(self, client: "TestClient") -> AuthResponse:
        response = client.post(
            url="/auth/register",
            json={
                "username": "fixtureUser",
                "password": "1234Abcd!@",
                "email": "fixtureUser@gmail.com",
            },
        )
        return AuthResponse(**response.json())

    def _request(
        self,
        client: "TestClient",
        fixture_user: AuthResponse,
        old_password: str,
        password: str,
    ) -> "Response":
        return client.patch(
            url=self._PATH,
            headers={"Authorization": fixture_user["access_token"]},
            json={
                "old_password": old_password,
                "password": password,
            },
        )

    def test_password_change(
        self,
        client: "TestClient",
        fixture_user: AuthResponse,
    ) -> None:
        response = self._request(client, fixture_user, "1234Abcd!@", "1234Abcd!@Efg")

        assert response.status_code == 200

    def test_password_equals_current(
        self,
        client: "TestClient",
        fixture_user: AuthResponse,
    ) -> None:
        response = self._request(client, fixture_user, "1234Abcd!@", "1234Abcd!@")

        assert response.status_code == 400
        assert response.json()["className"] == "PasswordEqualsToCurrentError"

    def test_passwords_do_not_match(
        self,
        client: "TestClient",
        fixture_user: AuthResponse,
    ) -> None:
        response = self._request(client, fixture_user, "1234Abcd!@@a", "1234Abcd!@Efg")

        assert response.status_code == 400
        assert response.json()["className"] == "PasswordsDoNotMatchError"

    def test_password_already_used(
        self,
        client: "TestClient",
        fixture_user: AuthResponse,
    ) -> None:
        response = self._request(client, fixture_user, "1234Abcd!@", "1234Abcd!@Efg")

        assert response.status_code == 200

        response = self._request(client, fixture_user, "1234Abcd!@Efg", "1234Abcd!@")

        assert response.status_code == 409
        assert response.json()["className"] == "PasswordAlreadyUsedError"
