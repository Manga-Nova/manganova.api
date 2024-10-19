from typing import TYPE_CHECKING, Any

from fastapi.responses import JSONResponse

from src._translator import Translator
from src._types import LanguageEnum

if TYPE_CHECKING:
    from fastapi import Request


class ApiError(Exception):
    """Base class for API exceptions."""

    _translator = Translator()

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        **metadata: str | float | bool | dict[str, Any] | list[Any],
    ) -> None:
        self.className = self.__class__.__name__
        self.message = message
        self.statusCode = status_code
        self.metadata = {**metadata}
        super().__init__(message)

    @staticmethod
    async def handler(request: "Request", exc: "ApiError") -> JSONResponse:
        """Handle an API error."""

        def _get_language() -> str:
            lang = request.headers.get("Use-Language", None)
            return lang if lang and lang in LanguageEnum else "en"

        exc.message = await ApiError._translator.translate(
            key=f"err-{exc.className}",
            language=_get_language(),
            **exc.metadata,
        )
        return JSONResponse(
            status_code=exc.statusCode,
            content={
                "className": exc.className,
                "statusCode": exc.statusCode,
                "message": exc.message,
                "metadata": exc.metadata,
            },
        )
