from typing import TYPE_CHECKING, TypedDict

from sqlalchemy import func, select

from src.modules.base.repository import BaseRepository
from src.modules.rating.model import RatingTable

if TYPE_CHECKING:
    from src.modules.rating.dtos import CreateRating


class _RatingResponse(TypedDict):
    """Rating response model."""

    ratings: dict[int, int]
    average: float


class RatingRepository(BaseRepository):
    async def get_rating(self, title_id: int) -> _RatingResponse:
        """Get a rating by specified filters."""

        async with self._session() as session:
            query = (
                select(RatingTable.value, func.count(RatingTable.value))
                .where(
                    RatingTable.title_id == title_id,
                )
                .group_by(RatingTable.value)
            )
            result = (await session.execute(query)).all()

            rating_counts = {int(key): int(value) for key, value in result}

            total_ratings = sum(rating_counts.values())
            weighted_sum = sum(value * count for value, count in rating_counts.items())

            average_rating = weighted_sum / total_ratings if total_ratings > 0 else 0

            return {
                "ratings": rating_counts,
                "average": average_rating,
            }

    async def create_rating(self, params: "CreateRating") -> RatingTable:
        return await self._save(RatingTable(**params.model_dump()))
