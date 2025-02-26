import csv
import datetime
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as so

from minosreports.context import Context
from minosreports.db.models import Assignment, Shift, Station, Volunteer

context = Context.get(fallback_to_class=True)
logger = context.logger


def parse_affectations_csv(filename: Path, session: so.Session):
    count_rows: int = 0
    with open(filename, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            count_rows += 1
            if row["Volontaire"].strip():
                volunteer = get_volunteer(row["Volontaire"])
                stmt = (
                    sa.select(Volunteer)
                    .where(
                        sa.func.lower(Volunteer.firstname)
                        == volunteer.firstname.lower()
                    )
                    .where(
                        sa.func.lower(Volunteer.lastname) == volunteer.lastname.lower()
                    )
                )
                volunteer_in_db = session.execute(stmt).scalar_one_or_none()
                if volunteer_in_db is None:
                    logger.debug(
                        f"Adding volunteer {volunteer.firstname} "
                        f"{volunteer.lastname}"
                    )
                    session.add(volunteer)
                    volunteer_in_db = session.execute(stmt).scalar_one()
            else:
                volunteer_in_db = None

            bad_row = False
            for field in [
                "Nom DPS",
                "Date",
                "Début de poste",
                "Fin de poste",
                "Qualification",
            ]:
                if not row[field].strip():
                    logger.warning(f"Ignoring line without '{field}'")
                    bad_row = True
                    break
            if bad_row:
                continue

            station = get_station(nom_dps=row["Nom DPS"])
            stmt = sa.select(Station).where(Station.label == station.label)
            station_in_db = session.execute(stmt).scalar_one_or_none()
            if station_in_db is None:
                logger.debug(f"Adding station {station.label}")
                session.add(station)
                station_in_db = session.execute(stmt).scalar_one()

            shift = get_shift(
                station=station_in_db,
                date=row["Date"],
                debut_de_poste=row["Début de poste"],
                fin_de_poste=row["Fin de poste"],
            )
            stmt = (
                sa.select(Shift)
                .where(Shift.station == shift.station)
                .where(Shift.start_date_time == shift.start_date_time)
                .where(Shift.end_date_time == shift.end_date_time)
            )
            shift_in_db = session.execute(stmt).scalar_one_or_none()
            if shift_in_db is None:
                logger.debug(
                    f"Adding shift from {shift.start_date_time} to "
                    f"{shift.end_date_time} for {shift.station.label}"
                )
                session.add(shift)
                shift_in_db = session.execute(stmt).scalar_one()

            assignment = Assignment(role=row["Qualification"])
            assignment.shift = shift_in_db
            assignment.volunteer = volunteer_in_db
            if volunteer := assignment.volunteer:
                logger.debug(
                    f"Adding assignment of {volunteer.firstname} "
                    f"{volunteer.lastname} as {assignment.role} for "
                    f"{assignment.shift.station.label} from "
                    f"{assignment.shift.start_date_time} to "
                    f"{assignment.shift.end_date_time}"
                )
            else:
                logger.debug(
                    f"Adding missing assignment for {assignment.role} for "
                    f"{assignment.shift.station.label} from "
                    f"{assignment.shift.start_date_time} to "
                    f"{assignment.shift.end_date_time}"
                )
            session.add(assignment)

    return {"countRows": count_rows}


def get_volunteer(value: str) -> Volunteer:
    splits = value.split(" ")
    return Volunteer(
        firstname=splits[1] if len(splits) > 1 else "",
        lastname=splits[0],
        nivol=None,
        dt=None,
        locality=None,
        phone_number=None,
        email=None,
        minor=None,
        roles=None,
        incoming_date_time=None,
        incoming_transportation_system=None,
        incoming_train_station=None,
        outgoing_date_time=None,
        outgoing_transportation_system=None,
        outgoing_train_station=None,
        crf_transportation_type=None,
    )


def get_station(nom_dps: str) -> Station:
    return Station(label=nom_dps)


def get_shift(
    station: Station, date: str, debut_de_poste: str, fin_de_poste: str
) -> Shift:
    date_splits = [int(value) for value in date.split("/")]
    debut_splits = [int(value) for value in debut_de_poste.split(":")]
    fin_splits = [int(value) for value in fin_de_poste.split(":")]

    start_day = datetime.datetime(  # noqa: DTZ001
        day=date_splits[0],
        month=date_splits[1],
        year=date_splits[2],
        hour=debut_splits[0],
        minute=debut_splits[1],
    )
    end_day = datetime.datetime(  # noqa: DTZ001
        day=date_splits[0],
        month=date_splits[1],
        year=date_splits[2],
        hour=fin_splits[0],
        minute=fin_splits[1],
    )
    if end_day < start_day:
        end_day += datetime.timedelta(days=1)
    shift = Shift(start_date_time=start_day, end_date_time=end_day)
    shift.station = station
    return shift
