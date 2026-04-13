"""Customer application / use-case layer.

**Input**
  ``CustomerCreate`` has already run: UK email/phone rules, stripping, HTML escape
  on free text. This layer trusts that contract.

**Responsibility**
  - Build ``Customer`` ORM objects and call the **repository** only (no raw SQL).
  - **HTTP semantics:** map ``get_by_id`` → ``None`` to ``404`` via
    ``HTTPException``. The repository never raises HTTP exceptions.
  - **Enrichment:** ``_build_response_data`` simulates downstream processing (e.g.
    credit scoring, KYC). In production this would call external APIs; here it
    returns a deterministic string so tests stay stable.

**Why ``_build_response_data`` is a module function**
  Pure, stateless helper — easy to test and to swap for a real integration later.

**Class**
  ``CustomerService`` holds a ``CustomerRepository`` created with the same session
  as the request — transactions stay scoped to ``get_session``.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerListResponse, CustomerResponse, CustomerSubmitResponse


def _build_response_data(payload: CustomerCreate) -> str:
    """Simulated enrichment result stored in ``response_data``.

    Production: replace with calls to scoring/verification services. Tests rely on
    a predictable string. ``payload.name`` / ``request_details`` are already
    HTML-escaped in ``CustomerCreate`` — do not escape again (avoid double-encoding).
    """
    return (
        f"Processed request for {payload.name} "
        f"({payload.email}); details length={len(payload.request_details)} chars."
    )


class CustomerService:
    """Use-case facade — see module docstring for layering and 404 handling."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = CustomerRepository(session)

    async def create_customer(self, payload: CustomerCreate) -> CustomerSubmitResponse:
        entity = Customer(
            name=payload.name,
            email=str(payload.email),
            phone=payload.phone,
            request_details=payload.request_details,
            response_data=_build_response_data(payload),
        )
        saved = await self._repo.create(entity)
        return CustomerSubmitResponse(id=saved.id)

    async def get_customer(self, customer_id: UUID) -> CustomerResponse:
        row = await self._repo.get_by_id(customer_id)
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return CustomerResponse.model_validate(row)

    async def list_customers(self, *, limit: int, offset: int) -> CustomerListResponse:
        rows, total = await self._repo.list_paginated(limit=limit, offset=offset)
        return CustomerListResponse(
            items=[CustomerResponse.model_validate(r) for r in rows],
            total=total,
            limit=limit,
            offset=offset,
        )
