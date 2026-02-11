from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    
    # API KEY
    OPEN_AI_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 1025

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
