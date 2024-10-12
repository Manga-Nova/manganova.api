from collections.abc import Sequence
from typing import Annotated

from fastapi import Body, Query, Request

from src.core.router import ApiRouter
from src.modules.group.dtos import CreateGroup, GetGroups, Group
from src.modules.group.repository import GroupRepository
from src.modules.group.service import GroupService
from src.modules.user.dtos import User

router = ApiRouter(prefix="/group", tags=["group"])

SERVICE = GroupService(GroupRepository())


@router.get("", response_model=Sequence[Group])
async def get_groups(params: Annotated[GetGroups, Query()]) -> Sequence[Group]:
    return await SERVICE.get_groups(params)


@router.post(path="", response_model=Group, requires_login=True)
async def create_group(
    request: Request,
    params: Annotated[CreateGroup, Body()],
) -> Group:
    return await SERVICE.create_group(user_id=request.state.user.id, params=params)


@router.get("/{group_id}/members", response_model=Sequence[User])
async def get_group_members(group_id: int) -> Sequence["User"]:
    return await SERVICE.get_group_members(group_id)


@router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int) -> Group:
    return await SERVICE.get_group(group_id)


@router.get("/{group_id}/follow", requires_login=True)
async def check_user_follow(group_id: int, request: Request) -> bool:
    return await SERVICE.check_user_follow(group_id, request.state.user.id)


@router.post("/{group_id}/follow", requires_login=True, status_code=201)
async def follow_group(group_id: int, request: Request) -> None:
    return await SERVICE.follow_group(group_id, request.state.user.id)


@router.delete("/{group_id}/follow", requires_login=True, status_code=204)
async def unfollow_group(group_id: int, request: Request) -> None:
    return await SERVICE.unfollow_group(group_id, request.state.user.id)
