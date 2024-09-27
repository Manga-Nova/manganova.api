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

    EMAIL_MIN_LENGTH: int = 4
    EMAIL_MAX_LENGTH: int = 256
    EMAIL_REGEX: str = r"^(?=.{4,256}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 256
    PASSWORD_SPECIAL_CHARS: str = "@$!%*?&"
    PASSWORD_REGEX: str = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,256}$"
    )

    USERNAME_MIN_LENGTH: int = 4
    USERNAME_MAX_LENGTH: int = 30
    USERNAME_REGEX: str = r"^[a-zA-Z0-9_\.]{3,50}$"


Settings = _Settings()
