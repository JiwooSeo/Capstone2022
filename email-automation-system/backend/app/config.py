from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    # App
    debug: bool = True
    environment: str = "development"
    app_title: str = "Email Automation & Scheduling System"
    app_version: str = "0.1.0"

    # Database
    database_url: str

    # Gmail OAuth
    gmail_client_id: str
    gmail_client_secret: str
    gmail_redirect_uri: str

    # OpenAI
    openai_api_key: str

    # Security
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    encryption_key: str

    # Redis
    redis_url: Optional[str] = None

    # Email Processing
    email_fetch_limit: int = 50
    email_batch_size: int = 5
    scheduler_timezone: str = "UTC"

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Retention
    email_retention_days: int = 90

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
