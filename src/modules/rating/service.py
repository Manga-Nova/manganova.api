from typing import TYPE_CHECKING

from src.modules.rating.dtos import CreateRating, PostRating, Rating

if TYPE_CHECKING:
    from src.modules.rating.repository import RatingRepository


class RatingService:
    def __init__(self, rating_repository: "RatingRepository") -> None:
        self.repository = rating_repository

    async def get_rating(self, title_id: int) -> Rating:
        """Get a rating by ID."""
        rating = await self.repository.get_rating(title_id=title_id)

        return Rating(**rating)

    async def create_rating(
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

        await self.repository.create_rating(
            params=input_params,
        )

        return input_params

    async def delete_rating(self, title_id: int, user_id: int) -> None:
        """Delete a rating."""
        await self.repository.delete_rating(title_id=title_id, user_id=user_id)
