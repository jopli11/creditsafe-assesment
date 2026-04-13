"""API request/response models (Pydantic v2) — single source of truth for JSON shapes.

**CustomerCreate (POST body)**
  - **Email / phone:** Step-by-step validation via ``_email_validation_error`` and
    ``_uk_phone_validation_error`` — specific user-facing strings at each failure
    (not a generic “invalid”). The **same messages** are implemented in
    ``frontend/src/lib/customer-validation.ts`` so client and server stay aligned;
    the API remains authoritative for security.
  - **UK phone:** Normalises ``+44`` / ``44``… to a leading ``0``, checks length
    and prefixes (``07`` mobiles, ``01``/``02``/``03`` landlines, etc.).
  - **XSS:** ``html.escape`` on ``name`` and ``request_details`` after whitespace
    normalisation — mitigates **stored** XSS if data is ever rendered outside React
    (email, PDF, admin tools). Email is not HTML-escaped the same way (format checks
    already restrict characters).

**Responses**
  - ``CustomerSubmitResponse``: 201 payload with ``id`` + success metadata.
  - ``CustomerResponse``: ``from_attributes=True`` maps ORM rows for GET responses.
  - ``CustomerListResponse``: items + ``total`` / ``limit`` / ``offset`` for the table.

OpenAPI / ``/docs`` is generated from these models automatically.
"""

from __future__ import annotations

import html
import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_ALLOWED = re.compile(r"^[A-Za-z0-9.@_%+-]+$")
_EMAIL_FULL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _email_validation_error(value: str) -> str | None:
    v = value.strip()
    if not v:
        return "Email is required"
    if len(v) > 320:
        return "Email is too long"
    if "@" not in v:
        return "Email must include an @ between the name and the domain (e.g. alex@company.com)."
    at = v.find("@")
    if "@" in v[at + 1 :]:
        return "Use a single @ symbol (e.g. name@domain.com)."
    local, domain = v[:at], v[at + 1 :]
    if not local:
        return "Add something before the @ (your mailbox name, e.g. alex.smith)."
    if not domain:
        return "Add the domain after the @ (e.g. gmail.com or company.co.uk)."
    if "." not in domain:
        return "The domain after @ needs a dot (e.g. .com, .co.uk, or .org)."
    if domain.startswith(".") or domain.endswith("."):
        return "The domain cannot start or end with a dot."
    tld = domain.rsplit(".", maxsplit=1)[-1]
    if not re.fullmatch(r"[A-Za-z]{2,}", tld):
        return "The part after the last dot (like .com or .uk) must be at least 2 letters."
    if not _EMAIL_ALLOWED.fullmatch(v):
        return "Email can only use letters, numbers, and . @ _ % + -."
    if not _EMAIL_FULL.fullmatch(v):
        return "That does not look like a complete email yet — check spelling around the name and domain."
    return None


def _uk_phone_validation_error(value: str) -> str | None:
    v = value.strip()
    if not v:
        return "Phone number is required"
    if len(v) > 50:
        return "Phone number is too long"
    if not re.fullmatch(r"[\d\s\-+().]+", v):
        return (
            "Use only digits, spaces, hyphens, brackets, and +. "
            "Letters and other symbols are not valid in a phone number."
        )
    digits = re.sub(r"\D", "", v)
    if not digits:
        return "Enter at least one digit in your phone number."
    d = digits
    if d.startswith("44") and len(d) >= 10:
        d = "0" + d[2:]
    if not d.startswith("0"):
        return "Use a UK number starting with 0 (e.g. 020 7946 0958) or with +44 (e.g. +44 20 7946 0958)."
    if len(d) < 10:
        return "UK numbers need at least 10 digits including the leading 0. Add the rest of the number."
    if len(d) > 11:
        return "UK numbers are at most 11 digits including the leading 0. Check for extra digits."
    if d.startswith("07"):
        if len(d) != 11:
            return "UK mobile numbers are 11 digits long and start with 07 (e.g. 07700 900123)."
        if not re.fullmatch(r"07[1-9]\d{8}", d):
            return "After 07 the next digit should be 1–9 for a valid UK mobile."
        return None
    if re.match(r"^(01|02|03|05|08|09)", d):
        if len(d) < 10 or len(d) > 11:
            return (
                "That length does not match a typical UK landline or service number "
                "(expect 10–11 digits including the leading 0)."
            )
        return None
    return (
        "Use a valid UK format: mobiles start with 07; many landlines start with 01, 02, or 03. "
        "Include the leading 0 or use +44."
    )


def _strip_and_escape_free_text(value: str) -> str:
    """Normalize whitespace and escape HTML metacharacters for safe storage/display."""
    cleaned = " ".join(value.split())
    return html.escape(cleaned, quote=True)


class CustomerCreate(BaseModel):
    """Payload for POST /api/customers."""

    name: str = Field(min_length=1, max_length=255)
    email: str = Field(max_length=320)
    phone: str = Field(max_length=50)
    request_details: str = Field(min_length=1, max_length=10_000)

    @field_validator("name", "phone", "request_details")
    @classmethod
    def strip_outer_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, v: object) -> str:
        return str(v).strip() if v is not None else ""

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str) -> str:
        err = _email_validation_error(v)
        if err:
            raise ValueError(err)
        return v

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        err = _uk_phone_validation_error(v)
        if err:
            raise ValueError(err)
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
