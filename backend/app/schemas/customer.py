"""Request/response models for customer endpoints.

Validation mirrors the SRS: required fields, email format, and defensive
sanitization for stored text (mitigates reflected/stored XSS if data is shown
in a browser later).
"""

from __future__ import annotations

import html
import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

_PHONE_RE = re.compile(r"^[\d\s\-+().]{7,50}$")


def _strip_and_escape_free_text(value: str) -> str:
    """Normalize whitespace and escape HTML metacharacters for safe storage/display."""
    cleaned = " ".join(value.split())
    return html.escape(cleaned, quote=True)


class CustomerCreate(BaseModel):
    """Payload for POST /api/customers."""

    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=50)
    request_details: str = Field(min_length=1, max_length=10_000)

    @field_validator("name", "phone", "request_details")
    @classmethod
    def strip_outer_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        if not _PHONE_RE.match(v):
            raise ValueError("phone must contain only digits and common separators")
        return v

    @field_validator("name", "request_details")
    @classmethod
    def escape_text_fields(cls, v: str) -> str:
        return _strip_and_escape_free_text(v)


class CustomerSubmitResponse(BaseModel):
    """SRS success shape for customer submission."""

    model_config = ConfigDict(json_schema_extra={"example": {"id": "uuid", "status": "success"}})

    id: UUID
    status: str = Field(default="success")
    message: str = Field(default="Customer data stored successfully")


class CustomerResponse(BaseModel):
    """Single customer returned from GET /api/customers/{id}."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    phone: str
    request_details: str
    response_data: str
    created_at: datetime


class CustomerListResponse(BaseModel):
    """Paginated list of customers."""

    items: list[CustomerResponse]
    total: int
    limit: int
    offset: int
