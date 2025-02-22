from datetime import datetime
from types import MappingProxyType
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from sqlalchemy.sql.schema import MetaData


class Base(MappedAsDataclass, DeclarativeBase):
    # This map details the specific transformation of types between Python and
    # SQLite. This is only needed for the case where a specific SQLite
    # type has to be used or when we want to ensure a specific setting (like the
    # timezone below). It uses a MappingProxyType to make the dict immutable and
    # avoid strange side-effects (RUF012)
    type_annotation_map = MappingProxyType(
        {
            datetime: DateTime(
                timezone=False
            ),  # transform Python datetime into SQLAlchemy Datetime without timezone
        }
    )

    # This metadata specifies some naming conventions that will be used by
    # alembic to generate constraints names (indexes, unique constraints, ...)
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    pass


class Volunteer(Base):
    """A person volunteering on our event"""

    __tablename__ = "volunteer"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    firstname: Mapped[str] = mapped_column(index=True)
    lastname: Mapped[str] = mapped_column(index=True)
    locality: Mapped[str]
    minor: Mapped[bool]
    roles: Mapped[list[str]]

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="volunteer", cascade="all, delete-orphan", init=False
    )


class Station(Base):
    """A station, i.e. somewhere where volunteer needs to be affected"""

    __tablename__ = "station"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    label: Mapped[str] = mapped_column(index=True)

    shifts: Mapped[list["Shift"]] = relationship(
        back_populates="station", cascade="all, delete-orphan", init=False
    )


class Shift(Base):
    """A shift, i.e. a station time slots where volunteers needs to be affected"""

    __tablename__ = "shift"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    start_date_time: Mapped[datetime] = mapped_column(index=True)
    end_date_time: Mapped[datetime] = mapped_column(index=True)
    station_id: Mapped[int] = mapped_column(
        ForeignKey("station.id"), init=False, index=True
    )
    station: Mapped["Station"] = relationship(back_populates="shifts", init=False)

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="shift", cascade="all, delete-orphan", init=False
    )


class Assignment(Base):
    """An assignment on one station shift for a given role

    Assignment might be occupied (have a volunteer assigned) or clear (volunteer still
    to find)
    """

    __tablename__ = "assignment"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    volunteer_id: Mapped[int] = mapped_column(
        ForeignKey("volunteer.id"), init=False, index=True, nullable=True
    )
    volunteer: Mapped["Volunteer | None"] = relationship(
        back_populates="assignments", init=False
    )
    shift_id: Mapped[int] = mapped_column(
        ForeignKey("shift.id"), init=False, index=True
    )
    shift: Mapped["Shift"] = relationship(back_populates="assignments", init=False)
    role: Mapped[str] = mapped_column(index=True)
