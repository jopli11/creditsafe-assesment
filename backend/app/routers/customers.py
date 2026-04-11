"""Customer HTTP routes — thin layer; logic lives in services."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerSubmitResponse,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


def get_customer_service(
    session: AsyncSession = Depends(get_session),
) -> CustomerService:
    return CustomerService(session)


@router.post(
    "",
    response_model=CustomerSubmitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerSubmitResponse:
    return await service.create_customer(payload)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return await service.get_customer(customer_id)


@router.get("", response_model=CustomerListResponse)
async def list_customers(
    service: CustomerService = Depends(get_customer_service),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> CustomerListResponse:
    return await service.list_customers(limit=limit, offset=offset)
