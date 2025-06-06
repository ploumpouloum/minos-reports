"""add assignement comments

Revision ID: d12f0662bc0b
Revises: 4dd480915a98
Create Date: 2025-05-29 19:02:57.894210

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d12f0662bc0b"
down_revision: str | None = "4dd480915a98"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("assignment", sa.Column("comments", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("assignment", "comments")
    # ### end Alembic commands ###
