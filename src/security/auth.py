from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader

from src.exceptions.unauthorized import MissingTokenError


class AuthSecurity(APIKeyHeader):
    """Authorization security scheme."""

    def __init__(
        self,
        *,
        name: str = "Authorization",
        scheme_name: str = "Authorization",
        description: str = "Bearer token",
        auto_error: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    def _get_token(self, request: Request) -> str:
        """Get token from request."""
        if token := request.headers.get(self.model.name):
            return token
        raise MissingTokenError

    async def _validate(self, request: Request) -> None:
        """Validate token."""
        token = self._get_token(request)
        if token != "Bearer token":
            raise HTTPException(status_code=401, detail="Unauthorized")

    async def __call__(self, request: Request) -> None:
        """Check authorization header."""
        await self._validate(request)
