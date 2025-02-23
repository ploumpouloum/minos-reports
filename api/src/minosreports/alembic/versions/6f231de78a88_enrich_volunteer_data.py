"""enrich volunteer data

Revision ID: 6f231de78a88
Revises: 7b5ee2b93cde
Create Date: 2025-02-23 20:32:09.271148

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6f231de78a88"
down_revision: str | None = "7b5ee2b93cde"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("volunteer", sa.Column("locality", sa.String(), nullable=True))
    op.add_column("volunteer", sa.Column("minor", sa.Boolean(), nullable=True))
    op.add_column(
        "volunteer", sa.Column("roles", postgresql.ARRAY(sa.String()), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("volunteer", "roles")
    op.drop_column("volunteer", "minor")
    op.drop_column("volunteer", "locality")
    # ### end Alembic commands ###
