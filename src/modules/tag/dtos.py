from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from src.modules.tag.enums import TagGroupEnum


class Tag(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    group: TagGroupEnum
    is_active: bool


class CreateTag(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    group: TagGroupEnum


class UpdateTag(BaseModel):
    name: Annotated[str | None, Field(max_length=100)] = None


class GetTags(BaseModel):
    include_not_active: bool = False
