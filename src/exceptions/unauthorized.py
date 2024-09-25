from typing import Any

from fastapi import status

from src.exceptions.base import ApiError


class UnauthorizedError(ApiError):
    """Unauthorized exception."""

    def __init__(
        self,
        message: str = "Unauthorized",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, **metadata)


class MissingTokenError(UnauthorizedError):
    """Missing token exception."""

    def __init__(
        self,
        message: str = "Missing Token",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message=message, **metadata)
