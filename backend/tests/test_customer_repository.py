"""Repository tests: async SQLite in-memory, schema from ``Base.metadata``.

Exercises create/get/list without FastAPI — pure SQLAlchemy data access.
"""

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.base import Base
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.mark.asyncio
async def test_create_and_get_round_trip() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        repo = CustomerRepository(session)
        entity = Customer(
            name="N",
            email="e@x.co",
            phone="555",
            request_details="R",
            response_data="OK",
        )
        saved = await repo.create(entity)
        await session.commit()

        loaded = await repo.get_by_id(saved.id)
        assert loaded is not None
        assert loaded.email == "e@x.co"

    await engine.dispose()


@pytest.mark.asyncio
async def test_list_paginated_returns_total() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        repo = CustomerRepository(session)
        for i in range(3):
            await repo.create(
                Customer(
                    name=f"U{i}",
                    email=f"u{i}@x.co",
                    phone="555",
                    request_details="R",
                    response_data="OK",
                ),
            )
        await session.commit()

        page, total = await repo.list_paginated(limit=2, offset=0)
        assert total == 3
        assert len(page) == 2

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_unknown() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        repo = CustomerRepository(session)
        assert await repo.get_by_id(uuid4()) is None

    await engine.dispose()
