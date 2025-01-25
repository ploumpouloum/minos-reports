from datetime import datetime
from types import MappingProxyType
from uuid import UUID

from sqlalchemy import (
    DateTime,
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
    firstname: Mapped[str]
    lastname: Mapped[str]

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="volunteer", cascade="all, delete-orphan", init=False
    )


class Station(Base):
    """A station, i.e. somewhere where volunteer needs to be affected"""

    __tablename__ = "station"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    label: Mapped[str]
    startDateTime: Mapped[datetime]
    endDateTime: Mapped[datetime]

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="station", cascade="all, delete-orphan", init=False
    )


class Assignment(Base):
    """An assignment of one volunteer on one station for a given role"""

    __tablename__ = "assignment"
    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, server_default=text("uuid_generate_v4()")
    )
    volunteer: Mapped["Volunteer"] = relationship(back_populates="assignments", init=False)
    station: Mapped["Station"] = relationship(back_populates="assignments", init=False)
    role: Mapped[str]
