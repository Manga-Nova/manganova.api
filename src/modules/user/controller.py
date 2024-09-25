from typing import Annotated

from fastapi import Body, Path

from src.core.router import ApiRouter
from src.exceptions.not_found import UserNotFoundError
from src.modules.user.dtos import CreateUserDTO, ExportUserDTO
from src.modules.user.repository import UserRepository
from src.modules.user.service import UserService

router = ApiRouter(prefix="/user", tags=["user"])

SERVICE = UserService(UserRepository())


@router.get(
    path="/{user_id}",
    response_model=ExportUserDTO,
    exceptions=[UserNotFoundError(userId=1234)],
)
async def get_user_by_id(
    user_id: Annotated[int, Path()],
) -> ExportUserDTO:
    """Get a user by ID."""
    return await SERVICE.get_user_by_id(user_id)


@router.post(path="", response_model=ExportUserDTO)
async def create_user(user: Annotated[CreateUserDTO, Body()]) -> ExportUserDTO:
    """Create a user."""
    return await SERVICE.create_user(user)
