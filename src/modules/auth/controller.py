from typing import Annotated

from fastapi import Body, Request

from src.core.crypt import CryptHelper
from src.core.router import ApiRouter
from src.modules.auth.dtos import (
    ChangePasswordParams,
    LoginParams,
    LoginResponse,
    RegisterParams,
)
from src.modules.auth.repository import AuthRepository
from src.modules.auth.service import AuthService

router = ApiRouter(prefix="/auth", tags=["auth"])

SERVICE = AuthService(AuthRepository(), CryptHelper())


@router.post(path="/login")
async def login(params: Annotated[LoginParams, Body()]) -> LoginResponse:
    """Login with email and password."""
    return await SERVICE.login(params)


@router.post(path="/register")
async def register(params: Annotated[RegisterParams, Body()]) -> LoginResponse:
    """Register a new user."""
    return await SERVICE.register(params)


@router.post(path="/change-password", requires_login=True)
async def change_password(
    request: Request,
    params: Annotated[ChangePasswordParams, Body()],
) -> None:
    """Change the password of the current user."""
    return await SERVICE.change_password(request.state.user_id, params)
