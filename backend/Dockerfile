# Production-style API image: runtime deps only (no pytest). Layer order caches pip
# installs when only app code changes. Compose overrides CMD to run alembic then uvicorn.

FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY alembic.ini alembic.ini
COPY alembic ./alembic
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
