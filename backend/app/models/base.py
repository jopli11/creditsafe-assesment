"""Declarative SQLAlchemy base — shared metadata for Alembic and test ``create_all``."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Single registry: import models so Alembic autogenerate sees every table."""
