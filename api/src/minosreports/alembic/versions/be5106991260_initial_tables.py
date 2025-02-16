"""Initial tables

Revision ID: be5106991260
Revises:
Create Date: 2025-01-27 20:34:24.991372

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "be5106991260"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "station",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("label", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_station")),
    )
    op.create_index(op.f("ix_station_label"), "station", ["label"], unique=False)
    op.create_table(
        "volunteer",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("lastname", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_volunteer")),
    )
    op.create_index(
        op.f("ix_volunteer_firstname"), "volunteer", ["firstname"], unique=False
    )
    op.create_index(
        op.f("ix_volunteer_lastname"), "volunteer", ["lastname"], unique=False
    )
    op.create_table(
        "shift",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("startDateTime", sa.DateTime(), nullable=False),
        sa.Column("endDateTime", sa.DateTime(), nullable=False),
        sa.Column("station_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["station_id"], ["station.id"], name=op.f("fk_shift_station_id_station")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shift")),
    )
    op.create_index(
        op.f("ix_shift_endDateTime"), "shift", ["endDateTime"], unique=False
    )
    op.create_index(
        op.f("ix_shift_startDateTime"), "shift", ["startDateTime"], unique=False
    )
    op.create_index(op.f("ix_shift_station_id"), "shift", ["station_id"], unique=False)
    op.create_table(
        "assignment",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("volunteer_id", sa.Uuid(), nullable=True),
        sa.Column("shift_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shift_id"], ["shift.id"], name=op.f("fk_assignment_shift_id_shift")
        ),
        sa.ForeignKeyConstraint(
            ["volunteer_id"],
            ["volunteer.id"],
            name=op.f("fk_assignment_volunteer_id_volunteer"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assignment")),
    )
    op.create_index(op.f("ix_assignment_role"), "assignment", ["role"], unique=False)
    op.create_index(
        op.f("ix_assignment_shift_id"), "assignment", ["shift_id"], unique=False
    )
    op.create_index(
        op.f("ix_assignment_volunteer_id"), "assignment", ["volunteer_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_assignment_volunteer_id"), table_name="assignment")
    op.drop_index(op.f("ix_assignment_shift_id"), table_name="assignment")
    op.drop_index(op.f("ix_assignment_role"), table_name="assignment")
    op.drop_table("assignment")
    op.drop_index(op.f("ix_shift_station_id"), table_name="shift")
    op.drop_index(op.f("ix_shift_startDateTime"), table_name="shift")
    op.drop_index(op.f("ix_shift_endDateTime"), table_name="shift")
    op.drop_table("shift")
    op.drop_index(op.f("ix_volunteer_lastname"), table_name="volunteer")
    op.drop_index(op.f("ix_volunteer_firstname"), table_name="volunteer")
    op.drop_table("volunteer")
    op.drop_index(op.f("ix_station_label"), table_name="station")
    op.drop_table("station")
    # ### end Alembic commands ###
