"""``customers`` table — SQLAlchemy 2 declarative mapping.

**Why UUID PK (not serial)?**
  Opaque IDs, no row-count leakage, friendly to distributed / merged databases.

**Columns**
  - ``id``: Python ``uuid.uuid4`` default; ORM generates IDs before flush where needed.
  - ``email``: ``String(320)`` (RFC 5321 max), **indexed** for lookups (not unique
    in this schema — business could add uniqueness later).
  - ``created_at``: ``timezone=True`` + ``server_default=func.now()`` so the **database**
    clock owns “created” time (consistent across app instances, no skew).

**Separation from Pydantic**
  ORM types reflect storage; API validation and messages live in ``schemas/customer.py``.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Customer(Base):
    """ORM row for one customer submission + stored enrichment (`response_data`)."""

    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    request_details: Mapped[str] = mapped_column(Text, nullable=False)
    response_data: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
