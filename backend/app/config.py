"""Application configuration loaded from the environment (Pydantic Settings)."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # No Python defaults — single source of truth is env / .env (fail fast if missing)
    database_url: str = Field(..., alias="DATABASE_URL")
    cors_origins: str = Field(..., alias="CORS_ORIGINS")

    @field_validator("database_url")
    @classmethod
    def strip_database_url(cls, v: str) -> str:
        return v.strip()

    @property
    def cors_origin_list(self) -> list[str]:
        # Comma-separated string → list for CORSMiddleware (e.g. Vite on 5173)
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Parse env once per worker process."""
    return Settings()
