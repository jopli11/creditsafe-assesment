"""Customer data access — SQLAlchemy only (persistence layer).

**Design**
  No FastAPI imports, no ``HTTPException``. Callers interpret ``None`` and map to
  HTTP. Easy to mock in service tests and to swap databases behind the same API.

**``create``**
  ``add`` + ``flush`` persists the INSERT within the current transaction so
  server-side defaults (e.g. ``created_at``) exist; ``refresh`` reloads the row.
  **Commit** happens in ``get_session`` after the route returns — not here — so
  a failure later in the request rolls back the whole unit of work.

**``get_by_id`` / ``list_paginated``**
  ``scalar_one_or_none()`` for optional rows. List uses **two** queries: total
  count for pagination UI, then ``ORDER BY created_at DESC`` with ``limit``/``offset``.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    """CRUD for ``Customer`` rows — see module docstring for flush/commit split."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, customer: Customer) -> Customer:
        self._session.add(customer)
        await self._session.flush()
        await self._session.refresh(customer)
        return customer

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        result = await self._session.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()

    async def list_paginated(self, *, limit: int, offset: int) -> tuple[list[Customer], int]:
        count_result = await self._session.execute(select(func.count()).select_from(Customer))
        total = int(count_result.scalar_one())
        rows = await self._session.execute(
            select(Customer)
            .order_by(Customer.created_at.desc())
            .limit(limit)
            .offset(offset),
        )
        items = list(rows.scalars().all())
        return items, total
