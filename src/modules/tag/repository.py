from collections.abc import Sequence
from typing import Self

from sqlalchemy import select

from src.modules.base.repository import BaseRepository
from src.modules.tag.dtos import CreateTag, GetTags, UpdateTag
from src.modules.tag.table import TagTable


class TagRepository(BaseRepository):
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def get_tag(self, tag_id: int) -> TagTable | None:
        query = select(TagTable).filter(TagTable.id == tag_id)
        return (await self._execute_query(query)).first()

    async def get_tags(self, params: GetTags) -> Sequence[TagTable]:
        query = select(TagTable).where(TagTable.is_active)
        if params.include_not_active:
            query = select(TagTable)
        return (await self._execute_query(query)).all()

    async def get_tags_by_ids(self, tag_ids: Sequence[int]) -> Sequence[TagTable]:
        query = select(TagTable).where(TagTable.id.in_(tag_ids))
        return (await self._execute_query(query)).all()

    async def create_tag(self, params: CreateTag) -> TagTable:
        return await self._save(TagTable(**params.model_dump()))

    async def update_tag(
        self,
        tag: "TagTable",
        params: UpdateTag,
    ) -> TagTable:
        tag.update(params)
        return await self._save(tag)

    async def delete_tag(self, tag: "TagTable") -> None:
        async with self._session() as session:
            tag.is_active = False
            session.add(tag)
            await session.commit()
