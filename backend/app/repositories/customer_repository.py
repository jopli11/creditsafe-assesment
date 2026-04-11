"""Customer persistence — SQLAlchemy only; no business rules."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    """Encapsulates CRUD queries for `Customer` rows."""

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
