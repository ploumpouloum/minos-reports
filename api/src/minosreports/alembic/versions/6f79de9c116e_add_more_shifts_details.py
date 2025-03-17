"""add more shifts details

Revision ID: 6f79de9c116e
Revises: 4af09bee8e75
Create Date: 2025-03-16 20:36:55.098904

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f79de9c116e"
down_revision: str | None = "4af09bee8e75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("shift", sa.Column("meet_date_time", sa.DateTime(), nullable=False))
    op.add_column("shift", sa.Column("return_date_time", sa.DateTime(), nullable=False))
    op.create_index(
        op.f("ix_shift_meet_date_time"), "shift", ["meet_date_time"], unique=False
    )
    op.create_index(
        op.f("ix_shift_return_date_time"), "shift", ["return_date_time"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_shift_return_date_time"), table_name="shift")
    op.drop_index(op.f("ix_shift_meet_date_time"), table_name="shift")
    op.drop_column("shift", "return_date_time")
    op.drop_column("shift", "meet_date_time")
    # ### end Alembic commands ###
