"""Pydantic schema validation edge cases."""

import pytest
from pydantic import ValidationError

from app.schemas.customer import CustomerCreate


def test_customer_create_accepts_valid_payload() -> None:
    data = CustomerCreate(
        name="Jane Doe",
        email="jane@example.com",
        phone="+1 555-0100",
        request_details="Need a credit report for ACME Ltd.",
    )
    assert data.name == "Jane Doe"
    assert str(data.email) == "jane@example.com"


def test_customer_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError) as exc:
        CustomerCreate(
            name="X",
            email="not-an-email",
            phone="+1 555-0100",
            request_details="Details",
        )
    assert "email" in str(exc.value).lower()


def test_customer_create_rejects_bad_phone() -> None:
    with pytest.raises(ValidationError) as exc:
        CustomerCreate(
            name="X",
            email="a@b.co",
            phone="abc",
            request_details="Details",
        )
    assert "phone" in str(exc.value).lower()


def test_customer_create_escapes_html_in_text_fields() -> None:
    data = CustomerCreate(
        name="<script>alert(1)</script>",
        email="user@example.com",
        phone="5551234567",
        request_details="<b>bold</b>",
    )
    assert "<script>" not in data.name
    assert "&lt;script&gt;" in data.name
    assert "&lt;b&gt;" in data.request_details
