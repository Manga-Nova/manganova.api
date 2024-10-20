from typing import Any

from fastapi import status

from src.exceptions.base import ApiError


class UnauthorizedError(ApiError):
    """Unauthorized exception."""

    def __init__(
        self,
        message: str = "Unauthorized",
        **metadata: str | float | dict[str, Any] | list[Any],
    ) -> None:
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED, **metadata)


class MissingTokenError(UnauthorizedError):
    """Missing token exception."""

    def __init__(
        self,
        message: str = "Missing Token",
        **metadata: str | float | dict[str, Any] | list[Any],
    ) -> None:
        super().__init__(message=message, **metadata)


class InvalidTokenError(UnauthorizedError):
    """Invalid token exception."""

    def __init__(
        self,
        message: str = "Invalid Token",
        **metadata: str | float | dict[str, Any] | list[Any],
    ) -> None:
        super().__init__(message=message, **metadata)


class EmailOrPasswordError(UnauthorizedError):
    """Email or password error exception."""

    def __init__(
        self,
        message: str = "Email or password is incorrect",
        **metadata: str | float | dict[str, Any] | list[Any],
    ) -> None:
        super().__init__(message=message, **metadata)
