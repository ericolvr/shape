""" app configuration """
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """ app settings """
    
    db_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres" 

    app_name: str = "Shape API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    port: int = 8000

    secret_key: str = "change this"
    algorithm: str = "HS256"
    access_token_expires_in_minutes: int = 60

    log_level: str = "INFO"

    cors_origins: list[str] = ["http://localhost:3000",  "http://localhost:8000"]

    class Config:
        case_sensitive = False
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Singleton para configurações"""
    return Settings()