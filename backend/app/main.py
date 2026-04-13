"""FastAPI application factory.

**Why a factory (``create_app``)?**
  Returns a configured ``FastAPI`` instance — easy to test and avoids scattering
  side effects. ``app = create_app()`` is the ASGI entrypoint for uvicorn.

**What gets wired**
  - **CORS:** ``allow_origins`` from ``Settings.cors_origin_list`` so only browser
    origins you configure (e.g. the Vite dev server) can call the API from JS.
    ``allow_credentials`` + wildcard methods/headers keeps local dev simple;
    production would tighten these.
  - **Router:** ``customers.router`` mounted at ``prefix="/api"`` → all customer
    routes live under ``/api/customers``.
  - **``lifespan``:** Async context manager hook (FastAPI’s modern replacement for
    ``@app.on_event``). Empty for now; use for DB pool warm-up, metrics, etc.
  - **``redirect_slashes=False``:** Stops automatic ``/api/foo`` ↔ ``/api/foo/``
    redirects that confuse API clients.

OpenAPI title/description/version feed ``/docs`` (Swagger) automatically.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import customers


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Reserved for startup/shutdown hooks (e.g. cache warm-up)."""
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="Customer Information API",
        description="Accepts customer requests from React, validates, stores in PostgreSQL.",
        version="0.1.0",
        lifespan=lifespan,
        redirect_slashes=False,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(customers.router, prefix="/api")
    return application


app = create_app()
