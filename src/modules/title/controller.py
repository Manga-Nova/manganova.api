from collections.abc import Sequence
from typing import Annotated

from fastapi import Body, Path, Query, Request

from src.core.router import ApiRouter
from src.exceptions.conflict import TitleNameAlreadyExistsError
from src.exceptions.not_found import TagNotFoundError, TitleNotFoundError
from src.modules._rating_dto import CreateRating, PostRating, Rating
from src.modules.tag.repository import TagRepository
from src.modules.title.dtos import (
    CreateTitle,
    GetTitles,
    Title,
    UpdateTitle,
    UpdateTitleTags,
)
from src.modules.title.repository import TitleRepository
from src.modules.title.service import TitleService

router = ApiRouter(prefix="/title", tags=["title"])

SERVICE = TitleService(TitleRepository(), TagRepository())


@router.get(path="", response_model=Sequence[Title])
async def get_titles(params: Annotated[GetTitles, Query()]) -> Sequence[Title]:
    """Get all titles."""
    return await SERVICE.get_titles(params)


@router.post(path="", response_model=Title, exceptions=[TitleNameAlreadyExistsError()])
async def create_title(create_title: Annotated[CreateTitle, Body()]) -> Title:
    """Create a title."""
    return await SERVICE.create_title(create_title)


@router.get(path="/{title_id}", response_model=Title, exceptions=[TitleNotFoundError()])
async def get_title(title_id: Annotated[int, Path()]) -> Title:
    """Get a title by ID."""
    return await SERVICE.get_title(title_id)


@router.patch(
    path="/{title_id}",
    response_model=Title,
    exceptions=[TitleNotFoundError(), TitleNameAlreadyExistsError()],
)
async def update_title(
    title_id: Annotated[int, Path()],
    title: Annotated[UpdateTitle, Body()],
) -> Title:
    """Update a title."""
    return await SERVICE.update_title(title_id, title)


@router.delete(path="/{title_id}")
async def delete_title(title_id: Annotated[int, Path()]) -> None:
    """Delete a title."""
    await SERVICE.delete_title(title_id)


@router.patch(
    path="/{title_id}/tags",
    response_model=Title,
    exceptions=[TitleNotFoundError(), TagNotFoundError()],
)
async def add_title_tags(
    title_id: Annotated[int, Path()],
    params: Annotated[UpdateTitleTags, Body()],
) -> Title:
    """Add title tags."""
    return await SERVICE.add_tags(title_id, params)


@router.delete(
    path="/{title_id}/tags",
    response_model=Title,
    exceptions=[TitleNotFoundError(), TagNotFoundError()],
)
async def remove_title_tags(
    title_id: Annotated[int, Path()],
    params: Annotated[UpdateTitleTags, Body()],
) -> Title:
    """Remove title tags."""
    return await SERVICE.remove_tags(title_id, params)


@router.get("/{title_id}/rating", response_model=Rating)
async def get_title_rating(
    title_id: Annotated[int, Path()],
) -> Rating:
    """Get the rating for a title."""
    return await SERVICE.get_title_rating(title_id)


@router.post(path="/{title_id}/rating", response_model=CreateRating)
async def create_title_rating(
    request: Request,
    title_id: Annotated[int, Path()],
    params: Annotated[PostRating, Body()],
) -> CreateRating:
    """Create a rating for a title."""
    return await SERVICE.post_title_rating(request.state.user.id, title_id, params)


@router.delete(path="/{title_id}/rating", status_code=204)
async def delete_title_rating(
    request: Request,
    title_id: Annotated[int, Path()],
) -> None:
    """Delete a rating for a title."""
    await SERVICE.remove_title_rating(request.state.user.id, title_id)
