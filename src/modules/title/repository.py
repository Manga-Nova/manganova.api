from collections.abc import Sequence
from typing import TYPE_CHECKING, Self

from sqlalchemy import delete, func, select
from sqlalchemy.orm import joinedload

from src.modules._rating_dto import Rating
from src.modules.base.repository import BaseRepository
from src.modules.tag.table import TagTable
from src.modules.title.dtos import CreateTitle, GetTitles, UpdateTitle
from src.modules.title.table import TitleRatingTable, TitleTable

if TYPE_CHECKING:
    from src.modules._rating_dto import CreateRating


class TitleRepository(BaseRepository):
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def get_title(self, **filters: str | float) -> TitleTable | None:
        """Get a title by specified filters."""

        query = (
            select(TitleTable).filter_by(**filters).options(joinedload(TitleTable.tags))
        )
        return (await self._execute_query(query)).first()

    async def get_titles(self, params: GetTitles) -> Sequence[TitleTable]:
        """Get all titles."""
        query = (
            select(TitleTable).options(joinedload(TitleTable.tags)).limit(params.limit)
        )

        if params.name:
            query = query.filter(TitleTable.name.ilike(f"%{params.name}%"))

        if params.include_content:
            query = query.filter(TitleTable.content_type.in_(params.include_content))

        if params.exclude_content:
            query = query.filter(~TitleTable.content_type.in_(params.exclude_content))

        if params.include_tags:
            query = query.filter(
                TitleTable.tags.any(TagTable.id.in_(params.include_tags)),
            )

        if params.exclude_tags:
            query = query.filter(
                ~TitleTable.tags.any(TagTable.id.in_(params.exclude_tags)),
            )

        return (await self._execute_query(query)).unique().all()

    async def create_title(
        self,
        params: CreateTitle,
        tags: Sequence["TagTable"],
    ) -> TitleTable:
        return await self._save(
            TitleTable(**params.model_dump(exclude={"tags"}), tags=tags),
        )

    async def update_title(self, title: TitleTable, params: UpdateTitle) -> TitleTable:
        title.update(params)
        return await self._save(title)

    async def delete_title(self, title: TitleTable) -> None:
        async with self._session() as session:
            await session.delete(title)
            await session.commit()

    async def add_tags(
        self,
        title: TitleTable,
        tags: Sequence["TagTable"],
    ) -> TitleTable:
        title.tags = [tag for tag in tags if tag not in title.tags]
        return await self._save(title)

    async def remove_tags(
        self,
        title: TitleTable,
        tags: Sequence["TagTable"],
    ) -> TitleTable:
        title.tags = [tag for tag in title.tags if tag not in tags]
        return await self._save(title)

    async def get_title_by_name(self, name: str) -> TitleTable | None:
        query = select(TitleTable).filter(TitleTable.name == name)
        return (await self._execute_query(query)).first()

    async def get_title_rating(
        self,
        title_id: int,
    ) -> Rating:
        """Get a rating by specified filters."""

        async with self._session() as session:
            query = (
                select(TitleRatingTable.value, func.count(TitleRatingTable.value))
                .where(TitleRatingTable.target_id == title_id)
                .group_by(TitleRatingTable.value)
            )

            result = (await session.execute(query)).all()

            rating_counts = {int(key): int(value) for key, value in result}

            total_ratings = sum(rating_counts.values())
            weighted_sum = sum(value * count for value, count in rating_counts.items())

            average_rating = weighted_sum / total_ratings if total_ratings > 0 else 0

            return Rating(average=average_rating, ratings=rating_counts)

    async def create_title_rating(self, params: "CreateRating") -> "TitleRatingTable":
        return await self._save(TitleRatingTable(**params.model_dump()))

    async def delete_title_rating(self, title_id: int, user_id: int) -> None:
        smt = delete(TitleRatingTable).where(
            TitleRatingTable.target_id == title_id,
            TitleRatingTable.user_id == user_id,
        )
        await self._delete(smt)

    async def update_title_cover(self, title: TitleTable, cover: str) -> TitleTable:
        title.cover_image = cover
        return await self._save(title)
