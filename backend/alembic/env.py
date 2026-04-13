"""Alembic migration environment — async SQLAlchemy, URL from application settings.

**Why ``get_settings().database_url``?**
  One env var (``DATABASE_URL``) drives both **uvicorn** and **alembic upgrade**.
  The URL in ``alembic.ini`` is a placeholder only; ``env.py`` overwrites it so
  local, Docker, and CI never drift.

**Metadata**
  ``target_metadata = Base.metadata``. Importing ``app.models.customer`` registers
  the ``customers`` table for autogenerate.

**Online vs offline**
  - **Online:** ``async_engine_from_config`` + ``NullPool`` (migrations are
    short-lived; no need for a warm pool). ``run_sync`` bridges Alembic’s sync
    API to async connections.
  - **Offline:** SQL scripts with literal binds — for generating SQL files without DB.

**CLI entry:** ``run_migrations_online`` uses ``asyncio.run`` because the Alembic
process is synchronous at the top level.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import get_settings
from app.models.base import Base

# Import models so metadata is populated for autogenerate
from app.models import customer  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return get_settings().database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (SQL script generation)."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
