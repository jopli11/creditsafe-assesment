"""SQLAlchemy ``DeclarativeBase`` — one metadata registry for the whole app.

**Why it matters**
  - **Alembic:** ``target_metadata = Base.metadata`` in ``env.py``; autogenerate
    sees every model imported under ``app.models``.
  - **Tests:** ``Base.metadata.create_all()`` builds SQLite schema from the same
    definitions as Postgres (for integration tests).

All ORM classes inherit from ``Base`` so migrations and tests stay consistent.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base — see module docstring."""
