from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from src._version import get_version


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=None)

    ENV: Literal["prod", "dev", "test"] = "dev"

    APP_NAME: str = "Manga Nova API"
    APP_VERSION: str = get_version()

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    JWT_SECRET: str = "secret"


Settings = _Settings()
