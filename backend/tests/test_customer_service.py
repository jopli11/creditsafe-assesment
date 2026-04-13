"""Service tests with a mocked ``CustomerRepository`` (no real DB)."""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.services.customer_service import CustomerService


@pytest.mark.asyncio
async def test_create_customer_persists_via_repository() -> None:
    session = MagicMock()
    service = CustomerService(session)
    fake_id = uuid4()
    captured: dict = {}

    async def fake_create(customer: Customer) -> Customer:
        captured["customer"] = customer
        customer.id = fake_id
        return customer

    service._repo.create = AsyncMock(side_effect=fake_create)  # type: ignore[method-assign]

    payload = CustomerCreate(
        name="A",
        email="a@b.co",
        phone="07700900123",
        request_details="Hello",
    )
    result = await service.create_customer(payload)
    assert result.id == fake_id
    assert result.status == "success"
    assert "stored successfully" in result.message.lower()
    assert captured["customer"].response_data


@pytest.mark.asyncio
async def test_get_customer_raises_404_when_missing() -> None:
    session = MagicMock()
    service = CustomerService(session)
    service._repo.get_by_id = AsyncMock(return_value=None)  # type: ignore[method-assign]

    with pytest.raises(HTTPException) as exc:
        await service.get_customer(uuid4())
    assert exc.value.status_code == 404
