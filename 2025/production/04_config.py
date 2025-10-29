# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_url: str = "https://api.exchangerate.host/latest"
    sentry_dsn: str = ""
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()