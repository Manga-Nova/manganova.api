from typing import Annotated

from fastapi import Body, Path, Request

from src.core.router import ApiRouter
from src.modules.rating.dtos import CreateRating, PostRating, Rating
from src.modules.rating.repository import RatingRepository
from src.modules.rating.service import RatingService

router = ApiRouter(prefix="/rating", tags=["rating"])

SERVICE = RatingService(RatingRepository())


@router.get("/title/{title_id}", response_model=Rating)
async def get_title_rating(
    title_id: Annotated[int, Path()],
) -> Rating:
    """Get the rating for a rating."""
    return await SERVICE.get_title_rating(title_id)


@router.post(
    "/title/{title_id}",
    status_code=201,
    requires_login=True,
    response_model=CreateRating,
)
async def post_title_rating(
    request: Request,
    title_id: Annotated[int, Path()],
    params: Annotated[PostRating, Body()],
) -> CreateRating:
    """Create a rating for a rating."""
    return await SERVICE.create_title_rating(
        title_id=title_id,
        user_id=request.state.user.id,
        params=params,
    )


@router.delete("/title/{title_id}", status_code=204, requires_login=True)
async def delete_title_rating(
    request: Request,
    title_id: Annotated[int, Path()],
) -> None:
    """Delete a rating for a rating."""
    await SERVICE.delete_title_rating(title_id, request.state.user.id)
