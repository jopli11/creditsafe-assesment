"""Customer use-cases: orchestrate repository calls and HTTP semantics (e.g. 404)."""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerListResponse, CustomerResponse, CustomerSubmitResponse


def _build_response_data(payload: CustomerCreate) -> str:
    """Deterministic placeholder for downstream enrichment (tests depend on shape)."""
    return (
        f"Processed request for {payload.name} "
        f"({payload.email}); details length={len(payload.request_details)} chars."
    )


class CustomerService:
    """Facade over CustomerRepository for one request-scoped session."""

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
            # Repository returns None; HTTP mapping stays in the service layer
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
