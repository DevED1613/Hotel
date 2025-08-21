"""Fix booking table name

Revision ID: df28ed7ae6f3
Revises: cb212c261a5e
Create Date: 2025-05-28 13:09:55.145830
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "df28ed7ae6f3"
down_revision: Union[str, None] = "cb212c261a5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    if "bookings" in inspector.get_table_names():
        op.drop_table("bookings")
