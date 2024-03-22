from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/skypulse"
    test: bool = False
    project_name: str = "SkyPulse"


settings = Settings()  # type: ignore
