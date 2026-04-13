"""Initial revision: ``customers`` table + non-unique index on ``email``."""

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
    # Lookup/filter; product may add uniqueness later
    op.create_index(op.f("ix_customers_email"), "customers", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_customers_email"), table_name="customers")
    op.drop_table("customers")
