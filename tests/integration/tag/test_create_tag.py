from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from httpx import Response

    from tests.integration.models import AuthResponse


class TestTagSuite:
    _PATH = "/tag"

    @pytest.fixture(autouse=False)
    def fixture_tag(self, client: "TestClient", test_user: "AuthResponse") -> None:
        client.post(
            url=self._PATH,
            headers={"Authorization": f"Bearer {test_user['access_token']}"},
            json={
                "name": "Fixture Tag",
                "group": "GENRE",
            },
        )

    def _request_create_tag(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
        **kwargs: str,
    ) -> "Response":
        return client.post(
            url=self._PATH,
            headers={"Authorization": f"Bearer {test_user['access_token']}"},
            json=kwargs,
        )

    def _validate_create_tag(self, response: "Response", name: str, group: str) -> None:
        assert response.status_code == 200
        assert response.json()["name"] == name
        assert response.json()["group"] == group

    def test_create_genre_tag(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            name="Test Genre Tag",
            group="GENRE",
        )

        self._validate_create_tag(response, "Test Genre Tag", "GENRE")

    def test_create_theme_tag(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            name="Test Theme Tag",
            group="THEME",
        )

        self._validate_create_tag(response, "Test Theme Tag", "THEME")

    def test_create_format_tag(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            name="Test Format Tag",
            group="FORMAT",
        )
        self._validate_create_tag(response, "Test Format Tag", "FORMAT")

    def test_create_tag_invalid_group(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            name="Test Invalid Group Tag",
            group="INVALID",
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Input should be 'GENRE', 'THEME' or 'FORMAT'"
        )

    def test_create_tag_missing_name(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            group="GENRE",
        )

        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_create_tag_name_limit(
        self,
        client: "TestClient",
        test_user: "AuthResponse",
    ) -> None:
        response = self._request_create_tag(
            client,
            test_user,
            name="a" * 101,
            group="GENRE",
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "String should have at most 100 characters"
        )
