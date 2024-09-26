from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.modules.base.db_context import DatabaseContext


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Before startup
    await DatabaseContext.create_all()

    yield

    # Before shutdown
    await DatabaseContext.drop_all()
    await DatabaseContext.close_engine()
