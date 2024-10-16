from fastapi import FastAPI

from src._lifespan import lifespan
from src.exceptions.base import ApiError
from src.settings import Settings


def create_app() -> FastAPI:
    """Create a FastAPI application."""
    print("OLA" * 100)

    app = FastAPI(
        title=Settings.APP_NAME,
        version=Settings.APP_VERSION,
        lifespan=lifespan,
        exception_handlers={ApiError: ApiError.handler},
    )

    add_routes(app)

    return app


def add_routes(app: FastAPI) -> None:
    """Add routes to the application."""
    from src.modules.router import router

    app.include_router(router)
