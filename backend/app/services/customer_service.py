"""Customer use-cases: validation already applied by Pydantic; enrich and persist."""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerListResponse, CustomerResponse, CustomerSubmitResponse


def _build_response_data(payload: CustomerCreate) -> str:
    """Simulate downstream processing / enrichment (SRS: optionally enrich or transform).

    In production this might call an external scoring API; here we return a
    deterministic, human-readable summary suitable for demos and tests.

    Note: `payload.name` / `request_details` are already HTML-escaped at the schema
    layer for safe persistence; we do not escape again to avoid double-encoding.
    """
    return (
        f"Processed request for {payload.name} "
        f"({payload.email}); details length={len(payload.request_details)} chars."
    )


class CustomerService:
    """Coordinates repository access and HTTP-level errors."""

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
