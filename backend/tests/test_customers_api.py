"""End-to-end API tests through the ASGI stack."""

from uuid import UUID

import pytest


@pytest.mark.asyncio
async def test_post_customer_returns_201_and_uuid(async_client) -> None:
    resp = await async_client.post(
        "/api/customers",
        json={
            "name": "Pat Lee",
            "email": "pat@example.com",
            "phone": "+44 20 7946 0958",
            "request_details": "Please verify company registration.",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "success"
    UUID(body["id"])


@pytest.mark.asyncio
async def test_get_customer_after_create(async_client) -> None:
    create = await async_client.post(
        "/api/customers",
        json={
            "name": "Sam",
            "email": "sam@example.com",
            "phone": "5551234567",
            "request_details": "Need onboarding.",
        },
    )
    cid = create.json()["id"]

    get_one = await async_client.get(f"/api/customers/{cid}")
    assert get_one.status_code == 200
    data = get_one.json()
    assert data["email"] == "sam@example.com"
    assert data["response_data"]


@pytest.mark.asyncio
async def test_get_unknown_customer_404(async_client) -> None:
    resp = await async_client.get(
        "/api/customers/00000000-0000-4000-8000-000000000001",
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_customers_pagination(async_client) -> None:
    for i in range(5):
        r = await async_client.post(
            "/api/customers",
            json={
                "name": f"User{i}",
                "email": f"u{i}@example.com",
                "phone": "5551234567",
                "request_details": "x",
            },
        )
        assert r.status_code == 201

    page = await async_client.get("/api/customers", params={"limit": 2, "offset": 0})
    assert page.status_code == 200
    body = page.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2
    assert body["limit"] == 2
    assert body["offset"] == 0


@pytest.mark.asyncio
async def test_validation_error_on_bad_email(async_client) -> None:
    resp = await async_client.post(
        "/api/customers",
        json={
            "name": "X",
            "email": "bad",
            "phone": "5551234567",
            "request_details": "y",
        },
    )
    assert resp.status_code == 422
