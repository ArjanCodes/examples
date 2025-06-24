from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    debug: bool = False

    class Config:
        env_file = "settings.env"


settings = Settings()
print(f"Database URL: {settings.database_url}")
print(f"Debug mode: {settings.debug}")
