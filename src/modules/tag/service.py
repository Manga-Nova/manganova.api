from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.exceptions.bad_request import MissingParamsError
from src.exceptions.not_found import TagNotFoundError
from src.modules.tag.dtos import CreateTag, GetTags, Tag, UpdateTag

if TYPE_CHECKING:
    from src.modules.tag.repository import TagRepository


class TagService:
    def __init__(self, tag_repository: "TagRepository") -> None:
        self.repository = tag_repository

    async def get_tag(self, tag_id: int) -> Tag:
        """Get a tag by ID."""
        tag = await self.repository.get_tag(tag_id)

        if not tag:
            raise TagNotFoundError

        return Tag(**tag.__dict__)

    async def get_tags(self, params: GetTags) -> Sequence[Tag]:
        """Get all tags."""
        tags = await self.repository.get_tags(params)
        return [Tag(**tag.__dict__) for tag in tags]

    async def create_tag(self, create_tag: CreateTag) -> Tag:
        """Create a tag."""

        tag = await self.repository.create_tag(create_tag)
        return Tag(**tag.__dict__)

    async def update_tag(self, tag_id: int, update_tag: UpdateTag) -> Tag:
        """Update a tag."""
        if not update_tag.model_dump(exclude_unset=True):
            raise MissingParamsError

        tag = await self.repository.get_tag(tag_id)

        if not tag:
            raise TagNotFoundError

        tag = await self.repository.update_tag(tag, update_tag)
        return Tag(**tag.__dict__)

    async def delete_tag(self, tag_id: int) -> None:
        """Delete a tag."""
        tag = await self.repository.get_tag(tag_id)

        if not tag:
            raise TagNotFoundError

        await self.repository.delete_tag(tag)
