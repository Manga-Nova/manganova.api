from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.contexts.postgresql import PostgreSqlConnection


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Before startup
    await PostgreSqlConnection.create_all()

    yield

    # Before shutdown
    await PostgreSqlConnection.drop_all()
    await PostgreSqlConnection.close_engine()
