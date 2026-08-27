from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Syris AI JEE Study Companion"
    API_V1_STR: str = "/api/v1"
    
    # Database URL: defaults to local SQLite async, easily switched to PostgreSQL + asyncpg
    # Example PostgreSQL: postgresql+asyncpg://postgres:postgres@localhost:5432/syris_dev
    DATABASE_URL: str = "sqlite+aiosqlite:///./syris_dev.db"
    
    # Database connection pool settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return [v] if isinstance(v, str) else []

    # Security & limits
    MAX_PAYLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB limit for JSON/media payloads

    # AI Configuration (Dev Baseline)
    DEFAULT_AI_PROVIDER: str = "google"
    DEFAULT_AI_MODEL: str = "gemini-3.5-flash-lite"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
