from collections.abc import Sequence
from typing import TYPE_CHECKING

import magic
from fastapi import UploadFile

from src.core.contexts.aws_s3 import AwsContext
from src.core.validators import RegexValidator
from src.exceptions.bad_request import InvalidMimeTypeError
from src.exceptions.conflict import TitleNameAlreadyExistsError
from src.exceptions.not_found import TagNotFoundError, TitleNotFoundError
from src.modules._rating_dto import CreateRating, PostRating
from src.modules.tag.dtos import Tag
from src.modules.title.dtos import (
    CreateTitle,
    GetTitles,
    Title,
    UpdateTitle,
    UpdateTitleTags,
)
from src.settings import Settings

if TYPE_CHECKING:
    from src.modules._rating_dto import Rating
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
        self.aws_session = AwsContext.get_session()
        self.MIME = magic.Magic(mime=True)

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
        return Title(
            **title.model_dump(),
            tags=[Tag(**tag.model_dump()) for tag in tags],
        )

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

    async def get_title_rating(self, title_id: int) -> "Rating":
        """Get the rating for a title."""
        return await self.repository.get_title_rating(title_id)

    async def post_title_rating(
        self,
        user_id: int,
        title_id: int,
        params: PostRating,
    ) -> "CreateRating":
        """Post a rating for a title."""
        input_params = CreateRating(
            user_id=user_id,
            target_id=title_id,
            value=params.value,
        )
        await self.repository.create_title_rating(input_params)
        return input_params

    async def remove_title_rating(self, user_id: int, title_id: int) -> None:
        """Remove a rating for a title."""
        await self.repository.delete_title_rating(user_id, title_id)

    async def post_title_cover(self, title_id: int, file: UploadFile) -> str:
        """Post a cover for a title."""

        mime_type = file.content_type or self.MIME.from_buffer(await file.read(1024))

        RegexValidator(
            string=mime_type,
            regex=r"^image/(jpeg|webp|jpg|png|gif)$",
            exception=InvalidMimeTypeError(
                expectedMimeType="jpeg, webp, jpg, png, gif",
                mimeType=mime_type,
            ),
        )

        await file.seek(0)

        title = await self.repository.get_title(id=title_id)

        if not title:
            raise TitleNotFoundError

        file_blob = f"covers/{title_id}"

        async with self.aws_session.client("s3") as s3:  # type: ignore[no-untyped-call]
            await s3.upload_fileobj(  # type: ignore[no-untyped-call]
                file,
                Settings.AWS_BUCKET_NAME,
                file_blob,
                ExtraArgs={"ContentType": mime_type},
            )

        await self.repository.update_title_cover(title, file_blob)

        return f"s3://{file_blob}"
