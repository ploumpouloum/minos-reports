"""add volunteer dlus+department

Revision ID: 644a6aca09e0
Revises: 6f79de9c116e
Create Date: 2025-04-21 19:47:28.187319

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "644a6aca09e0"
down_revision: str | None = "6f79de9c116e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("volunteer", sa.Column("dlus_email", sa.String(), nullable=True))
    op.add_column("volunteer", sa.Column("department", sa.String(), nullable=True))
    op.drop_column("volunteer", "dt")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "volunteer", sa.Column("dt", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_column("volunteer", "department")
    op.drop_column("volunteer", "dlus_email")
    # ### end Alembic commands ###
