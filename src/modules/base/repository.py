from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from src.modules.base.model import ModelBase


class BaseRepository:
    """Base repository for all repositories."""

    _engine: AsyncEngine | None = None

    @staticmethod
    async def get_engine() -> AsyncEngine:
        """Get the engine."""
        if BaseRepository._engine is None:
            return await BaseRepository.create_engine()
        return BaseRepository._engine

    @staticmethod
    async def close_engine() -> None:
        """Close the engine."""
        if BaseRepository._engine is not None:
            await BaseRepository._engine.dispose()
            BaseRepository._engine = None

    @staticmethod
    async def create_engine() -> AsyncEngine:
        """Create the engine."""
        if BaseRepository._engine is not None:
            err_msg = (
                "AsyncEngine is already set. "
                "Use `BaseRepository.get_engine()` to get the engine."
            )
            raise ValueError(err_msg)

        from src.settings import Settings

        BaseRepository._engine = create_async_engine(Settings.postgres_url)
        return BaseRepository._engine

    @staticmethod
    async def create_all() -> None:
        """Create all tables."""
        engine = await BaseRepository.get_engine()

        async with engine.begin() as async_conn:
            await async_conn.run_sync(ModelBase.metadata.create_all)

    @staticmethod
    def session_maker() -> async_sessionmaker[AsyncSession]:
        """Get the session maker."""
        return async_sessionmaker(BaseRepository._engine, expire_on_commit=False)
