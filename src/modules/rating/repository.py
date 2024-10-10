from typing import TYPE_CHECKING, Self, TypedDict

from sqlalchemy import delete, func, select

from src.modules.base.repository import BaseRepository
from src.modules.rating.table import TitleRatingTable

if TYPE_CHECKING:
    from src.modules.rating.dtos import CreateRating

    class _RatingResponse(TypedDict):
        """Rating response model."""

        ratings: dict[int, int]
        average: float


class RatingRepository(BaseRepository):
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def get_title_rating(self, title_id: int) -> "_RatingResponse":
        """Get a rating by specified filters."""

        async with self._session() as session:
            query = (
                select(TitleRatingTable.value, func.count(TitleRatingTable.value))
                .where(
                    TitleRatingTable.title_id == title_id,
                )
                .group_by(TitleRatingTable.value)
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

    async def create_title_rating(self, params: "CreateRating") -> TitleRatingTable:
        return await self._save(TitleRatingTable(**params.model_dump()))

    async def delete_title_rating(self, title_id: int, user_id: int) -> None:
        smt = delete(TitleRatingTable).where(
            TitleRatingTable.title_id == title_id,
            TitleRatingTable.user_id == user_id,
        )
        await self._delete(smt)
