"""Pytest fixtures: SQLite in-memory + httpx ASGI client + dependency override.

**Why env vars before imports?**
  ``app.database`` builds the async engine at import time; ``Settings`` requires
  ``DATABASE_URL`` / ``CORS_ORIGINS``. ``setdefault`` supplies values for test runs
  when no ``.env`` is present (same URLs as local Postgres — the override replaces
  the actual DB with SQLite for requests).

**Fixtures**
  - ``db_engine`` / ``db_session``: in-memory ``aiosqlite``, schema via
    ``Base.metadata.create_all`` — real SQL, no mocks.
  - ``async_client``: ``httpx.AsyncClient`` + ``ASGITransport(app=app)`` hits the
    **real** FastAPI app in-process (no TCP). ``dependency_overrides[get_session]``
    swaps in a session factory backed by the test engine; commit/rollback mirrors
    production.

**Why httpx async, not Starlette ``TestClient``?**
  The app stack is fully async; sync test clients can block the event loop.

**Why SQLite not Postgres in tests?**
  Zero infra, sub-second runs; DI override still exercises router → service → repo.
"""

import os

# Settings and the DB engine initialize at import; env must be set first.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://app:app@localhost:5432/customers",
)
os.environ.setdefault(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import get_session
from app.main import app
from app.models.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_engine():
    """SQLite engine with schema created once per test function."""
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Session from the test engine; finer isolation can use `db_engine` directly."""
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(db_engine) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client hitting the ASGI app with overridden DB session."""
    session_factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
