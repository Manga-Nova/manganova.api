from collections.abc import Sequence
from typing import Annotated

from fastapi import Body, Path, Query

from src.core.router import ApiRouter
from src.exceptions.not_found import TagNotFoundError
from src.modules.tag.dtos import CreateTag, GetTags, Tag, UpdateTag
from src.modules.tag.repository import TagRepository
from src.modules.tag.service import TagService

router = ApiRouter(prefix="/tag", tags=["tag"])

SERVICE = TagService(TagRepository())


@router.get("", response_model=Sequence[Tag])
async def get_tags(params: Annotated[GetTags, Query()]) -> Sequence[Tag]:
    """Get all tags."""
    return await SERVICE.get_tags(params)


@router.get("/{tag_id}", response_model=Tag, exceptions=[TagNotFoundError()])
async def get_tag(tag_id: Annotated[int, Path()]) -> Tag:
    """Get a tag by ID."""
    return await SERVICE.get_tag(tag_id)


@router.post("", response_model=Tag, requires_login=True)
async def create_tag(tag: Annotated[CreateTag, Body()]) -> Tag:
    """Create a tag."""
    return await SERVICE.create_tag(tag)


@router.patch(
    "/{tag_id}",
    response_model=Tag,
    exceptions=[TagNotFoundError()],
    requires_login=True,
)
async def update_tag(
    tag_id: Annotated[int, Path()],
    tag: Annotated[UpdateTag, Body()],
) -> Tag:
    """Update a tag."""
    return await SERVICE.update_tag(tag_id, tag)


@router.delete(
    "/{tag_id}",
    exceptions=[TagNotFoundError()],
    status_code=204,
    requires_login=True,
)
async def delete_tag(tag_id: Annotated[int, Path()]) -> None:
    """Delete a tag."""
    await SERVICE.delete_tag(tag_id)
