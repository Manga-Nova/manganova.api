from sqlalchemy import select

from src.modules.base.repository import BaseRepository
from src.modules.user.model import User


class UserRepository(BaseRepository):
    """User repository."""

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""

        return (
            await self._execute_query(select(User).where(User.id == user_id))
        ).first()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        return (
            await self._execute_query(select(User).where(User.email == email))
        ).first()

    async def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        return (
            await self._execute_query(select(User).where(User.username == username))
        ).first()
