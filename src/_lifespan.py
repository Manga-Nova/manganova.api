from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.contexts.aws_s3 import AwsContext
from src.core.contexts.postgresql import PostgreSqlConnection
from src.settings import Settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Before startup
    await PostgreSqlConnection.create_all()

    if Settings.ENV == "dev":
        await AwsContext.create_bucket()

    yield

    # Before shutdown
    await PostgreSqlConnection.close_engine()
