from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    sentry_dsn: str = ""
    log_level: str = "INFO"
    database_url: str = "sqlite:///./db.sqlite3"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()