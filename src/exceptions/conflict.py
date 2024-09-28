from typing import Any

from src.exceptions.base import ApiError


class ConflictError(ApiError):
    def __init__(
        self,
        message: str = "Conflict",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message, 409, **metadata)


class UsernameAlreadyExistsError(ConflictError):
    def __init__(
        self,
        message: str = "Username already exists",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message=message, **metadata)


class PasswordAlreadyUsedError(ConflictError):
    def __init__(
        self,
        message: str = "Password already used",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message=message, **metadata)


class TitleNameAlreadyExistsError(ConflictError):
    def __init__(
        self,
        message: str = "Title name already exists",
        **metadata: str | float | dict[str, Any],
    ) -> None:
        super().__init__(message=message, **metadata)
