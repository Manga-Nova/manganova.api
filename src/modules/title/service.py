from collections.abc import Sequence
from typing import TYPE_CHECKING

from src.exceptions.conflict import TitleNameAlreadyExistsError
from src.exceptions.not_found import TagNotFoundError, TitleNotFoundError
from src.modules.title.dtos import (
    CreateTitle,
    GetTitles,
    Title,
    UpdateTitle,
    UpdateTitleTags,
)

if TYPE_CHECKING:
    from src.modules.tag.repository import TagRepository
    from src.modules.title.repository import TitleRepository


class TitleService:
    def __init__(
        self,
        title_repository: "TitleRepository",
        tag_repository: "TagRepository",
    ) -> None:
        self.repository = title_repository
        self.tag_repository = tag_repository

    async def get_title(self, title_id: int) -> Title:
        """Get a title by ID."""
        title = await self.repository.get_title(id=title_id)

        if not title:
            raise TitleNotFoundError

        return Title(**title.model_dump())

    async def get_titles(self, params: GetTitles) -> Sequence[Title]:
        """Get all titles."""
        titles = await self.repository.get_titles(params)
        return [Title(**title.model_dump()) for title in titles]

    async def create_title(self, create_title: CreateTitle) -> Title:
        """Create a title."""
        if await self.repository.get_title_by_name(create_title.name):
            raise TitleNameAlreadyExistsError

        tags = await self.tag_repository.get_tags_by_ids(create_title.tags)

        title = await self.repository.create_title(create_title, tags)
        return Title(**title.model_dump())

    async def update_title(self, title_id: int, update_title: UpdateTitle) -> Title:
        """Update a title."""
        title = await self.repository.get_title(id=title_id)

        if not title:
            raise TitleNotFoundError

        if update_title.name and await self.repository.get_title_by_name(
            update_title.name,
        ):
            raise TitleNameAlreadyExistsError

        title = await self.repository.update_title(title, update_title)
        return Title(**title.model_dump())

    async def delete_title(self, title_id: int) -> None:
        """Delete a title."""
        title = await self.repository.get_title(id=title_id)

        if not title:
            raise TitleNotFoundError

        await self.repository.delete_title(title)

    async def add_tags(self, title_id: int, params: UpdateTitleTags) -> Title:
        """Add a tag to a title."""
        title_ = await self.repository.get_title(id=title_id)

        if not title_:
            raise TitleNotFoundError

        tags = await self.tag_repository.get_tags_by_ids(params.tags)

        if not tags:
            raise TagNotFoundError

        title = await self.repository.add_tags(title_, tags)
        return Title(**title.model_dump())

    async def remove_tags(self, title_id: int, params: UpdateTitleTags) -> Title:
        """Remove a tag from a title."""
        title_ = await self.repository.get_title(id=title_id)

        if not title_:
            raise TitleNotFoundError

        tags = await self.tag_repository.get_tags_by_ids(params.tags)

        if not tags:
            raise TagNotFoundError

        title = await self.repository.remove_tags(title_, tags)
        return Title(**title.model_dump())
