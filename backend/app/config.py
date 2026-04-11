"""Application configuration loaded from environment variables.

We use Pydantic Settings so the same code works in Docker, local dev, and tests
(tests override env vars in fixtures).
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Default matches docker-compose local `db` service
    database_url: str = Field(
        default="postgresql+asyncpg://app:app@localhost:5432/customers",
        alias="DATABASE_URL",
    )

    # Comma-separated list of allowed browser origins for CORS
    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="CORS_ORIGINS",
    )

    @field_validator("database_url")
    @classmethod
    def strip_database_url(cls, v: str) -> str:
        return v.strip()

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — avoids re-parsing env on every request."""
    return Settings()
