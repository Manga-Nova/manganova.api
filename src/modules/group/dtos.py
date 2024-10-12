from pydantic import BaseModel

from src.modules.base.dtos import BaseDto
from src.modules.user.dtos import User


class CreateGroup(BaseModel):
    """Create group DTO."""

    name: str
    description: str | None


class GetGroups(BaseModel):
    """Get groups DTO."""

    name: str | None = None


class Group(BaseDto):
    name: str
    description: str | None
    owner_id: int
    followers: int = 0


class GroupWithOwner(Group):
    owner: User | None
