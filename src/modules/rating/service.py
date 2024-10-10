from typing import TYPE_CHECKING

from src.modules.rating.dtos import CreateRating, PostRating, Rating

if TYPE_CHECKING:
    from src.modules.rating.repository import RatingRepository


class RatingService:
    def __init__(self, rating_repository: "RatingRepository") -> None:
        self.repository = rating_repository

    async def get_title_rating(self, title_id: int) -> Rating:
        """Get a rating by ID."""
        rating = await self.repository.get_title_rating(title_id=title_id)

        return Rating(**rating)

    async def create_title_rating(
        self,
        title_id: int,
        user_id: int,
        params: PostRating,
    ) -> CreateRating:
        """Create a rating."""

        input_params = CreateRating(
            user_id=user_id,
            title_id=title_id,
            value=params.value,
        )

        await self.repository.create_title_rating(
            params=input_params,
        )

        return input_params

    async def delete_title_rating(self, title_id: int, user_id: int) -> None:
        """Delete a rating."""
        await self.repository.delete_title_rating(title_id=title_id, user_id=user_id)
