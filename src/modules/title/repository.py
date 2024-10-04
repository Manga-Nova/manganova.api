from collections.abc import Sequence
from typing import Self

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.modules.base.repository import BaseRepository
from src.modules.tag.model import TagTable
from src.modules.title.dtos import CreateTitle, GetTitles, UpdateTitle
from src.modules.title.model import TitleTable


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
