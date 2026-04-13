"""FastAPI app factory — ASGI (Asynchronous Server Gateway Interface) entrypoint for uvicorn (`app.main:app`)."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import customers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Hook for startup/shutdown (pool warm-up, metrics, etc.)."""
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="Customer Information API",
        description="Accepts customer requests from React, validates, stores in PostgreSQL.",
        version="0.1.0",
        lifespan=lifespan,
        # Avoid automatic trailing-slash redirects that confuse API clients
        redirect_slashes=False,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # All customer routes live under /api/customers
    application.include_router(customers.router, prefix="/api")
    return application


app = create_app()
