from fastapi import FastAPI

from src._lifespan import lifespan
from src.exceptions.base import ApiError
from src.settings import Settings


def create_app() -> FastAPI:
    """Create a FastAPI application."""
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
    from src.modules.user.controller import router as user_router

    app.include_router(user_router)
