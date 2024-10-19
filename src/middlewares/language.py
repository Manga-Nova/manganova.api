from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src._types import LanguageEnum
from src.exceptions.bad_request import InvalidLanguageError


class LanguageController(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Callable[
            [
                MutableMapping[str, Any],
                Callable[[], Awaitable[MutableMapping[str, Any]]],
                Callable[[MutableMapping[str, Any]], Awaitable[None]],
            ],
            Awaitable[None],
        ],
        dispatch: Callable[
            [Request, Callable[[Request], Awaitable[Response]]],
            Awaitable[Response],
        ]
        | None = None,
    ) -> None:
        super().__init__(app, dispatch)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        lang = request.headers.get("Use-Language", None)

        if lang and lang not in LanguageEnum:
            raise InvalidLanguageError(language=lang)

        response = await call_next(request)

        if lang and lang in LanguageEnum:
            response.headers["Use-Language"] = lang

        return response
