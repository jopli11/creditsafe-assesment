"""Revision 001 — create ``customers`` + index on ``email``.

**Schema alignment**
  Columns match ``app.models.customer`` so ORM and migration stay in sync (UUID PK,
  string lengths, ``Text`` for long fields, timezone-aware ``created_at`` with
  ``server_default`` — DB-generated timestamp).

**Index**
  Non-unique index on ``email`` for lookup/filter workloads; uniqueness not enforced
  here (product decision).

**Rollback**
  ``downgrade`` drops index then table — reversible for dev/staging resets.
"""

# Revision metadata (Alembic)
# Revision ID: 001
# Revises:
# Create Date: 2025-01-01

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("request_details", sa.Text(), nullable=False),
        sa.Column("response_data", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_email"), "customers", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_customers_email"), table_name="customers")
    op.drop_table("customers")
