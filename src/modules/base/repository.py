from typing import Any, TypeVar

from sqlalchemy import ScalarResult, Select

from src.core.contexts.postgresql import PostgreSqlConnection
from src.modules.base.model import ModelBaseTable

_T = TypeVar("_T", bound=Any)
_M = TypeVar("_M", bound=ModelBaseTable)


class BaseRepository:
    _session = PostgreSqlConnection.session_maker()

    async def _execute_query(self, query: Select[tuple[_T]]) -> ScalarResult[_T]:
        """Helper method to execute a query and return the result."""
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars()

    async def _save(self, model: _M) -> _M:
        """Saves a model."""
        async with self._session() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
        return model
