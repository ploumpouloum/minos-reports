import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import sqlalchemy as sa
import sqlalchemy.orm as so

from minosreports.context import Context
from minosreports.db.models import Volunteer

context = Context.get(fallback_to_class=True)
logger = context.logger


def parse_volontaires_csv(filename: Path, session: so.Session):
    count_rows: int = 0
    with open(filename, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            count_rows += 1

            bad_row = False
            for field in [
                "NIVOL",
                "Nom",
                "Prénom",
            ]:
                if not row[field].strip():
                    logger.warning(f"Ignoring line without '{field}'")
                    bad_row = True
                    break
            if bad_row:
                continue

            volunteer = get_volunteer(row)
            stmt = sa.select(Volunteer).where(
                (
                    sa.func.lower(Volunteer.firstname) == volunteer.firstname.lower()
                    and sa.func.lower(Volunteer.lastname) == volunteer.lastname.lower()
                )
                or Volunteer.nivol == volunteer.nivol
            )
            volunteer_in_db = session.execute(stmt).scalar_one_or_none()
            if volunteer_in_db is None:
                logger.debug(
                    f"Adding volunteer {volunteer.firstname} {volunteer.lastname}"
                )
                session.add(volunteer)
                volunteer_in_db = session.execute(stmt).scalar_one()

            else:
                volunteer_in_db.firstname = volunteer.firstname
                volunteer_in_db.lastname = volunteer.lastname
                volunteer_in_db.nivol = volunteer.nivol
                volunteer_in_db.locality = volunteer.locality
                volunteer_in_db.phone_number = volunteer.phone_number
                volunteer_in_db.email = volunteer.email
                volunteer_in_db.minor = volunteer.minor
                volunteer_in_db.roles = volunteer.roles
                volunteer_in_db.incoming_date_time = volunteer.incoming_date_time
                volunteer_in_db.incoming_transportation_system = (
                    volunteer.incoming_transportation_system
                )
                volunteer_in_db.incoming_train_station = (
                    volunteer.incoming_train_station
                )
                volunteer_in_db.outgoing_date_time = volunteer.outgoing_date_time
                volunteer_in_db.outgoing_transportation_system = (
                    volunteer.outgoing_transportation_system
                )
                volunteer_in_db.outgoing_train_station = (
                    volunteer.outgoing_train_station
                )
                volunteer_in_db.crf_transportation_type = (
                    volunteer.crf_transportation_type
                )
                volunteer_in_db.dlus_email = volunteer.dlus_email
                volunteer_in_db.department = volunteer.department

    return {"countRows": count_rows}


def get_volunteer(row: dict[str, Any]) -> Volunteer:
    def parse_restrictions(raw_data: str) -> list[str] | None:
        if not raw_data.strip():
            return None
        return [restriction.strip() for restriction in raw_data.split(",")]

    return Volunteer(
        firstname=row["Prénom"],
        lastname=row["Nom"],
        nivol=row["NIVOL"],
        locality=row["Structure locale"],
        phone_number=row["N° TEL"],
        email=row["E-MAIL"],
        minor=(row["Etes-vous ?"].lower() == "mineur"),
        roles=row["TOUTES vos qualifications"].split(", "),
        mission_restrictions=parse_restrictions(row["Ne souhaite pas participer :"]),
        food_restrictions=parse_restrictions(row["Précision regime particulier"]),
        incoming_date_time=(
            datetime.strptime(  # noqa: DTZ007
                row["Date et heure d'arrivée"], "%d/%m/%Y %H:%M"
            )
            if row["Date et heure d'arrivée"]
            else None
        ),
        incoming_transportation_system=row["Moyen de transport"],
        incoming_train_station=row["Gare SNCF arrivée"],
        outgoing_date_time=(
            datetime.strptime(  # noqa: DTZ007
                row["Date et heure de départ"], "%d/%m/%Y %H:%M"
            )
            if row["Date et heure de départ"]
            else None
        ),
        outgoing_transportation_system=row["Moyen de transport retour"],
        outgoing_train_station=row["Gare de retour"],
        crf_transportation_type=row["Si moyen CRF, Type :"],
        dlus_email=str(row["Mail NOMINATIF CRf du DLUS/RUS"]).strip().lower(),
        department=row["DT de rattachement"],
    )
