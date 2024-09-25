from typing import Any

from src.exceptions.base import ApiError


class NotFoundError(ApiError):
    """Not found error."""

    def __init__(
        self,
        message: str = "Resource not found.",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message, 404, **metadata)


class UserNotFoundError(NotFoundError):
    """User not found error."""

    def __init__(
        self,
        message: str = "User not found.",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message=message, **metadata)
