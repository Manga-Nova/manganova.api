from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel

from src.modules.tag.dtos import Tag
from src.modules.title.enums import TitleContentTypeEnum


class Title(BaseModel):
    """Title model."""

    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    description: str | None
    release_date: datetime | None
    tags: Sequence[Tag]
    content_type: TitleContentTypeEnum


class CreateTitle(BaseModel):
    """Create title model."""

    name: str
    description: str | None = None
    release_date: datetime | None = None
    tags: Sequence[int]
    content_type: TitleContentTypeEnum


class UpdateTitle(BaseModel):
    """Update title model."""

    name: str | None = None
    description: str | None = None
    release_date: datetime | None = None
    content_type: TitleContentTypeEnum | None = None


class GetTitles(BaseModel):
    """Get titles model."""

    name: str | None = None
    include_tags: Sequence[int] = []
    exclude_tags: Sequence[int] = []
    include_content: Sequence[TitleContentTypeEnum] = []
    exclude_content: Sequence[TitleContentTypeEnum] = []
    limit: int = 10


class UpdateTitleTags(BaseModel):
    """Update title tags model."""

    tags: Sequence[int]
