"""Async SQLAlchemy 2 engine and request-scoped sessions.

**Why async end-to-end?**
  FastAPI routes and asyncpg are async. Sync DB calls in a request would block the
  event loop and hurt throughput under load.

**Engine**
  - ``pool_pre_ping=True``: before handing out a pooled connection, SQLAlchemy
    pings it so stale connections (after Postgres restart, network blip) are
    discarded instead of failing mid-query.
  - ``echo=False``: SQL logging off in production; turn on for debugging.

**Session factory**
  ``expire_on_commit=False``: after ``commit``, ORM rows used in responses stay
  usable without lazy loads that could trigger IO after commit.

**``get_session`` dependency**
  Async generator: ``yield`` hands the session to the route; after the handler
  finishes, ``commit()`` on success or ``rollback()`` on any exception. That is the
  **unit-of-work** pattern — one transaction per HTTP request.

**Note:** Engine is created at import time (``get_settings()`` runs once). Tests
  override ``get_session`` so they do not hit production Postgres.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

_settings = get_settings()
engine = create_async_engine(
    _settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a DB session for the request; commit on success, rollback on errors."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
