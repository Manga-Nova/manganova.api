from pydantic_settings import BaseSettings, SettingsConfigDict

from src._version import get_version


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=None)

    APP_NAME: str = "Manga Nova API"
    APP_VERSION: str = get_version()

    POSTGRE_USER: str = "postgres"
    POSTGRE_PASSWORD: str = "postgres"
    POSTGRE_HOST: str = "localhost"
    POSTGRE_PORT: int = 5432
    POSTGRE_DB: str = "postgres"

    @property
    def postgre_url(self) -> str:
        return f"postgresql://{self.POSTGRE_USER}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_HOST}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"


Settings = _Settings()
