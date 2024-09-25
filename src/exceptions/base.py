from typing import Any


class ApiError(Exception):
    """Base class for API exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        **metadata: str | float | dict[str, Any],
    ) -> None:
        self.className = self.__class__.__name__
        self.message = message
        self.statusCode = status_code
        self.metadata = {**metadata}
        super().__init__(message)
