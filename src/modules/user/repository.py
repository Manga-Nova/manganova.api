from sqlalchemy import select

from src.modules.base.repository import BaseRepository
from src.modules.user.dtos import CreateUserDTO
from src.modules.user.model import User


class UserRepository(BaseRepository):
    """User repository."""

    _session = BaseRepository.session_maker()

    async def create_user(self, create_user: CreateUserDTO) -> User:
        """Create a user."""
        async with self._session() as session:
            user = User(**create_user.model_dump())
            session.add(user)
            await session.commit()
            return user

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
