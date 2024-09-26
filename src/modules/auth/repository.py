from collections.abc import Sequence

from sqlalchemy import select

from src.modules.auth.dtos import RegisterParams
from src.modules.auth.model import OldHash
from src.modules.base.repository import BaseRepository
from src.modules.user.dtos import UpdateUserDTO
from src.modules.user.model import User


class AuthRepository(BaseRepository):
    async def create_user(self, create_user: RegisterParams) -> User:
        """Create a user."""
        async with self._session() as session:
            user = User(**create_user.model_dump())
            session.add(user)
            await session.commit()
            return user

    async def update_user(self, user: User, update_user: UpdateUserDTO) -> User:
        """Update a user."""
        async with self._session() as session:
            for key, value in update_user.model_dump(exclude_defaults=True).items():
                setattr(user, key, value)
            await session.commit()
            return user

    async def update_user_password(self, user: User, new_password: str) -> None:
        """Update a user's password."""
        async with self._session() as session:
            old_hash = OldHash(user_id=user.id, password=user.password)
            session.add(old_hash)
            user.password = new_password
            session.add(user)
            await session.commit()

    async def get_user(self, **filters: str | float) -> User | None:
        """Get a user by specified filters."""
        query = select(User).filter_by(**filters)
        return (await self._execute_query(query)).first()

    async def get_user_by_email_or_username(
        self,
        email: str,
        username: str,
    ) -> User | None:
        """Get a user by email or username."""
        query = select(User).where((User.email == email) | (User.username == username))
        return (await self._execute_query(query)).first()

    async def get_old_passwords(self, user_id: int) -> Sequence[OldHash]:
        """Get old passwords of a user."""
        query = select(OldHash).where(OldHash.user_id == user_id)
        return (await self._execute_query(query)).all()
