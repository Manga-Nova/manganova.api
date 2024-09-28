from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.modules.base.model import ModelBaseTable
from src.settings import Settings


class DatabaseContext:
    """Database Context Manager"""

    _engine: AsyncEngine | None = None

    @staticmethod
    def get_engine() -> AsyncEngine:
        """Get the engine."""
        if DatabaseContext._engine is None:
            return DatabaseContext.create_engine()
        return DatabaseContext._engine

    @staticmethod
    async def close_engine() -> None:
        """Close the engine."""
        if DatabaseContext._engine is not None:
            await DatabaseContext._engine.dispose()
            DatabaseContext._engine = None

    @staticmethod
    def create_engine() -> AsyncEngine:
        """Create the engine."""
        if DatabaseContext._engine is not None:
            err_msg = (
                "AsyncEngine is already set. "
                "Use `DatabaseContext.get_engine()` to get the engine."
            )
            raise ValueError(err_msg)

        from src.settings import Settings

        DatabaseContext._engine = create_async_engine(Settings.postgres_url)
        return DatabaseContext._engine

    @staticmethod
    async def create_all() -> None:
        """Create all tables."""
        engine = DatabaseContext.get_engine()

        async with engine.begin() as async_conn:
            await async_conn.run_sync(ModelBaseTable.metadata.create_all)

    @staticmethod
    async def drop_all() -> None:
        """Drop all tables."""
        if not Settings.DB_DROP_TABLES:
            return

        engine = DatabaseContext.get_engine()

        async with engine.begin() as async_conn:
            await async_conn.run_sync(ModelBaseTable.metadata.drop_all)

    @staticmethod
    def session_maker() -> async_sessionmaker[AsyncSession]:
        """Get the session maker."""
        return async_sessionmaker(DatabaseContext.get_engine(), expire_on_commit=False)
