from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.exceptions.not_found import GroupNotFoundError
from src.modules.group.dtos import CreateGroup, GetGroups, Group
from src.modules.user.dtos import User

if TYPE_CHECKING:
    from src.modules.group.repository import GroupRepository


class GroupService:
    def __init__(self, group_repository: "GroupRepository") -> None:
        self.repository = group_repository

    async def get_groups(self, params: GetGroups) -> Sequence[Group]:
        return [
            Group(**data.model_dump())
            for data in await self.repository.get_groups(params)
        ]

    async def create_group(self, user_id: int, params: CreateGroup) -> Group:
        return Group(
            **(
                await self.repository.create_group(user_id=user_id, params=params)
            ).model_dump(),
        )

    async def get_group(self, group_id: int) -> Group:
        if group := await self.repository.get_group_by_id(group_id):
            return group

        raise GroupNotFoundError

    async def get_group_members(self, group_id: int) -> Sequence["User"]:
        return [
            User(**data.model_dump())
            for data in await self.repository.get_group_members(group_id)
        ]

    async def check_user_follow(self, group_id: int, user_id: int) -> bool:
        return await self.repository.check_user_follow(group_id, user_id)

    async def follow_group(self, group_id: int, user_id: int) -> None:
        if await self.repository.check_user_follow(group_id, user_id):
            return None
        return await self.repository.follow_group(group_id, user_id)

    async def unfollow_group(self, group_id: int, user_id: int) -> None:
        if not await self.repository.check_user_follow(group_id, user_id):
            return None
        return await self.repository.unfollow_group(group_id, user_id)
