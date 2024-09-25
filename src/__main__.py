from fastapi import FastAPI

from src.settings import Settings


def create_app() -> FastAPI:
    """Create a FastAPI application."""
    return FastAPI(
        title=Settings.APP_NAME,
        version=Settings.APP_VERSION,
        separate_input_output_schemas=True,
    )
