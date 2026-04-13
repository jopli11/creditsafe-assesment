"""Application configuration from the environment.

**Why Pydantic Settings (not raw ``os.getenv``)?**
  Typed fields, validation at import time, and ``.env`` loading in one place. Missing
  required vars fail fast with a clear error instead of ``None`` at runtime.

**Behaviour**
  - ``DATABASE_URL`` / ``CORS_ORIGINS`` use ``Field(...)`` — no Python defaults, so
    there is no second source of truth beside env / ``.env``.
  - ``env_file=".env"`` loads ``backend/.env`` when you run from ``backend/``;
    Docker Compose passes the same keys via ``environment:`` (no file needed).
  - ``strip_database_url`` trims accidental whitespace from pasted connection strings.
  - ``cors_origin_list`` splits the comma-separated env string for ``CORSMiddleware``
    (e.g. Vite on ``localhost:5173`` and ``127.0.0.1:5173``).

**Performance**
  ``@lru_cache`` on ``get_settings()`` parses env once per process, not per request.
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

    database_url: str = Field(..., alias="DATABASE_URL")
    cors_origins: str = Field(..., alias="CORS_ORIGINS")

    @field_validator("database_url")
    @classmethod
    def strip_database_url(cls, v: str) -> str:
        return v.strip()

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide ``Settings`` singleton (parse ``.env`` once per worker)."""
    return Settings()
