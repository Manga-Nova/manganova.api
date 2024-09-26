from sqlalchemy import select

from src.modules.base.db_context import DatabaseContext
from src.modules.user.model import User


class UserRepository:
    """User repository."""

    _session = DatabaseContext.session_maker()

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""
        async with self._session() as session:
            return (
                (await session.execute(select(User).where(User.id == user_id)))
                .scalars()
                .first()
            )

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        async with self._session() as session:
            return (
                (await session.execute(select(User).where(User.email == email)))
                .scalars()
                .first()
            )

    async def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        async with self._session() as session:
            return (
                (await session.execute(select(User).where(User.username == username)))
                .scalars()
                .first()
            )
