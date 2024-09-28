from typing import Any, TypeVar

from sqlalchemy import ScalarResult, Select

from src.core.contexts.postgresql import PostgreSqlConnection

_T = TypeVar("_T", bound=Any)


class BaseRepository:
    _session = PostgreSqlConnection.session_maker()

    async def _execute_query(self, query: Select[tuple[_T]]) -> ScalarResult[_T]:
        """Helper method to execute a query and return the result."""
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars()
