from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App metadata
    PROJECT_NAME: str = "RetailPulse"
    API_V1_PREFIX: str = "/api/v1"

    # Database connection string
    # This comes from your Supabase connection string
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
