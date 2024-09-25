from typing import TYPE_CHECKING

from src.modules.user.dtos import CreateUserDTO, ExportUserDTO

if TYPE_CHECKING:
    from src.modules.user.repository import UserRepository


class UserService:
    """User service."""

    def __init__(self, user_repository: "UserRepository") -> None:
        self.user_repository = user_repository

    async def create_user(self, create_user: CreateUserDTO) -> ExportUserDTO:
        """Create a user."""
        user_ = await self.user_repository.create_user(create_user)
        return ExportUserDTO(**user_.__dict__)

    async def get_user_by_id(self, user_id: str) -> ExportUserDTO:
        """Get a user by ID."""
        user_ = await self.user_repository.get_user_by_id(user_id)
        return ExportUserDTO(**user_.__dict__)
