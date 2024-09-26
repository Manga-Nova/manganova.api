from typing import Any, TypeVar

from sqlalchemy import ScalarResult, Select

from src.modules.base.db_context import DatabaseContext

_T = TypeVar("_T", bound=Any)


class BaseRepository:
    _session = DatabaseContext.session_maker()

    async def _execute_query(self, query: Select[tuple[_T]]) -> ScalarResult[_T]:
        """Helper method to execute a query and return the result."""
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars()
