import csv
import datetime
import re
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as so

from minosreports.context import Context
from minosreports.db.models import Assignment, Shift, Station, Volunteer

context = Context.get(fallback_to_class=True)
logger = context.logger

DPS_RE = re.compile(
    r"^(?P<day>\d{2})\/(?P<month>\d{2})\/(?P<year>\d{4}) de (?P<meet_hours>\d{2}):"
    r"(?P<meet_mins>\d{2}) à (?P<end_hours>\d{2}):(?P<end_mins>\d{2}) pour"
    r"\s*(?P<dps_name>.*?)\s*$"
)


def parse_affectations_csv(filename: Path, session: so.Session):
    count_rows: int = 0
    with open(filename, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            count_rows += 1

            bad_row = False
            for field in [
                "DPS",
                "Début de poste",
                "Qualification",
            ]:
                if not row[field].strip():
                    logger.warning(f"Ignoring row {count_rows}, missing '{field}'")
                    bad_row = True
                    break
            if bad_row:
                continue

            dps_match = DPS_RE.match(row["DPS"])
            if not dps_match:
                logger.warning(f"Ignoring row {count_rows}, 'DPS' field is incorrect")
                continue

            station = get_station(dps_match=dps_match)
            stmt = sa.select(Station).where(Station.label == station.label)
            station_in_db = session.execute(stmt).scalar_one_or_none()
            if station_in_db is None:
                logger.debug(f"Adding station {station.label}")
                session.add(station)
                station_in_db = session.execute(stmt).scalar_one()

            shift = get_shift(
                station=station_in_db,
                dps_match=dps_match,
                debut_de_poste=row["Début de poste"],
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

            nivol = row["NIVOL"].strip()
            if not nivol:
                volunteer_in_db = None
            else:
                stmt = sa.select(Volunteer).where(Volunteer.nivol == nivol)
                volunteer_in_db = session.execute(stmt).scalar_one_or_none()
                if volunteer_in_db is None:
                    logger.warning(f"NIVOL {nivol} is unknown")

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
        locality=None,
        phone_number=None,
        email=None,
        minor=None,
        roles=None,
        mission_restrictions=None,
        food_restrictions=None,
        incoming_date_time=None,
        incoming_transportation_system=None,
        incoming_train_station=None,
        outgoing_date_time=None,
        outgoing_transportation_system=None,
        outgoing_train_station=None,
        crf_transportation_type=None,
        dlus_email=None,
        department=None,
    )


def get_station(dps_match: re.Match[str]) -> Station:
    return Station(label=dps_match.group("dps_name"))


def get_shift(station: Station, dps_match: re.Match[str], debut_de_poste: str) -> Shift:

    debut_splits = [int(value) for value in debut_de_poste.split(":")]

    day = int(dps_match.group("day"))
    month = int(dps_match.group("month"))
    year = int(dps_match.group("year"))

    meet = datetime.datetime(  # noqa: DTZ001
        day=day,
        month=month,
        year=year,
        hour=int(dps_match.group("meet_hours")),
        minute=int(dps_match.group("meet_mins")),
    )

    start = datetime.datetime(  # noqa: DTZ001
        day=day,
        month=month,
        year=year,
        hour=debut_splits[0],
        minute=debut_splits[1],
    )

    end = datetime.datetime(  # noqa: DTZ001
        day=day,
        month=month,
        year=year,
        hour=int(dps_match.group("end_hours")),
        minute=int(dps_match.group("end_mins")),
    )

    if end < start:
        end += datetime.timedelta(days=1)
    shift = Shift(
        meet_date_time=meet,
        start_date_time=start,
        end_date_time=end,
        return_date_time=end,  # TODO: retrieve/compute this property
    )
    shift.station = station
    return shift
