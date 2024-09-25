from typing import Annotated

from fastapi import Body, Path

from src.core.router import ApiRouter
from src.modules.user.dtos import CreateUserDTO, ExportUserDTO
from src.modules.user.repository import UserRepository
from src.modules.user.service import UserService

router = ApiRouter(prefix="/user", tags=["user"])

SERVICE = UserService(UserRepository())


@router.get(path="/{userId}", requires_login=True)
async def get_user_by_id(userId: Annotated[str, Path()]) -> ExportUserDTO:
    """Get a user by ID."""
    return await SERVICE.get_user_by_id(userId)


@router.post(path="")
async def create_user(user: Annotated[CreateUserDTO, Body()]) -> ExportUserDTO:
    """Create a user."""
    return await SERVICE.create_user(user)
