from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = ""
    log_level: str = "INFO"
    database_url: str = "sqlite:///./db.sqlite3"

    model_config = ConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
