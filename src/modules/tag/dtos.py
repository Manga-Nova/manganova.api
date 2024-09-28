from datetime import datetime

from pydantic import BaseModel

from src.modules.tag.enums import TagGroupEnum


class Tag(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    group: TagGroupEnum
    is_active: bool


class CreateTag(BaseModel):
    name: str
    group: TagGroupEnum


class UpdateTag(BaseModel):
    name: str | None = None


class GetTags(BaseModel):
    include_not_active: bool = False
