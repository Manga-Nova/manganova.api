from collections.abc import Sequence
from typing import TYPE_CHECKING, Self

from sqlalchemy import delete, func, select
from sqlalchemy.orm import joinedload

from src.modules.base.repository import BaseRepository
from src.modules.group.dtos import CreateGroup, GetGroups, Group
from src.modules.group.table import GroupFollowersTable, GroupTable

if TYPE_CHECKING:
    from src.modules.user.table import UserTable


class GroupRepository(BaseRepository):
    """Group repository."""

    __instance: Self | None = None

    def __new__(cls) -> Self:
        """Create a new instance of the class."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def get_group_by_id(self, group_id: int) -> Group | None:
        """Get a group by its ID."""
        async with self._session() as session:
            query = (
                select(GroupTable, func.count(GroupTable.followers))
                .where(GroupTable.id == group_id)
                .options(joinedload(GroupTable.owner))
            )
            if result := (await session.execute(query)).first():
                table, count = result
                return Group(**table.model_dump(), followers=count)
            return None

    async def create_group(self, user_id: int, params: CreateGroup) -> GroupTable:
        """Create a new group."""
        return await self._save(GroupTable(**params.model_dump(), owner_id=user_id))

    async def get_groups(self, params: GetGroups) -> Sequence[GroupTable]:
        """Get groups."""
        query = select(GroupTable)

        if params.name:
            query = query.where(GroupTable.name.ilike(f"%{params.name}%"))

        return (await self._execute_query(query)).all()

    async def delete_group(self, group_id: int, user_id: int) -> None:
        """Delete a group by its ID."""
        smt = delete(GroupTable).where(
            GroupTable.id == group_id,
            GroupTable.owner_id == user_id,
        )
        await self._delete(smt)

    async def get_group_members(self, group_id: int) -> Sequence["UserTable"]:
        """Get group members."""
        query = (
            select(GroupTable)
            .where(GroupTable.id == group_id)
            .options(joinedload(GroupTable.members))
        )
        response = (await self._execute_query(query)).first()
        return response.members if response else []

    async def get_group_followers(self, group_id: int) -> Sequence["UserTable"]:
        """Get group followers."""
        query = (
            select(GroupTable)
            .where(GroupTable.id == group_id)
            .options(joinedload(GroupTable.followers))
        )
        response = (await self._execute_query(query)).first()
        return response.followers if response else []

    async def check_user_follow(self, group_id: int, user_id: int) -> bool:
        """Check if a user follows a group."""
        query = select(GroupFollowersTable).where(
            GroupFollowersTable.group_id == group_id,
            GroupFollowersTable.user_id == user_id,
        )
        return bool((await self._execute_query(query)).first())

    async def follow_group(self, group_id: int, user_id: int) -> None:
        """Follow a group."""
        await self._save(GroupFollowersTable(group_id=group_id, user_id=user_id))

    async def unfollow_group(self, group_id: int, user_id: int) -> None:
        """Unfollow a group."""
        smt = delete(GroupFollowersTable).where(
            GroupFollowersTable.group_id == group_id,
            GroupFollowersTable.user_id == user_id,
        )
        await self._delete(smt)
