import tempfile
from http import HTTPStatus
from pathlib import Path
from typing import Annotated

import sqlalchemy as sa
import sqlalchemy.orm as so
from fastapi import Cookie, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from minosreports.cloudflare_access import InvalidTokenError, verify_token
from minosreports.context import Context
from minosreports.db import dbsession
from minosreports.db.models import (
    Assignment,
    Shift,
    Station,
    StationKind,
    Volunteer,
    VolunteerStatus,
)
from minosreports.parsing.affectations import parse_affectations_csv
from minosreports.parsing.volontaires import parse_volontaires_csv

Context.setup()

context = Context.get(fallback_to_class=True)
logger = context.logger

app = FastAPI(root_path=context.api_root_path)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_cf_authorization(
    CF_Authorization: Annotated[str | None, Cookie()] = None,  # noqa: N803
):
    if not CF_Authorization:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Missing authorization cookie")
    try:
        claims = verify_token(CF_Authorization)
    except InvalidTokenError:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "Invalid authorization cookie"
        ) from None
    if not claims:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "No claims found in authorization cookie"
        )
    email = claims.get("email", None)
    if not email:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "No email claim found in authorization cookie"
        )
    return email


@app.get("/")
async def root(user_email: str = Depends(verify_cf_authorization)):
    return {"message": f"Hello {user_email}"}


@app.get("/whoami")
async def whoami(user_email: str = Depends(verify_cf_authorization)):
    return user_email


@app.get("/data")
async def data(user_email: str = Depends(verify_cf_authorization)):

    @dbsession
    def data_inner(session: so.Session):  # pyright: ignore[reportUnknownParameterType]

        is_supervisor = user_email in context.supervisor_mails
        is_dlus = (
            session.execute(
                sa.select(Volunteer).where(Volunteer.dlus_email == user_email)
            ).first()
            is not None
        )

        if is_supervisor:
            volunteers_stmt = sa.select(Volunteer, VolunteerStatus.arrived).join(
                VolunteerStatus,
                onclause=VolunteerStatus.nivol == Volunteer.nivol,
                isouter=True,
            )
            assignements_stmt = sa.select(Assignment)
            shifts_stmt = sa.select(Shift)
            stations_stmt = sa.select(Station, StationKind.kind).join(
                StationKind, onclause=StationKind.label == Station.label, isouter=True
            )
        else:
            volunteers_subquery = sa.select(Volunteer.id).where(
                sa.or_(
                    Volunteer.dlus_email == user_email, Volunteer.email == user_email
                )
            )
            assignements_subquery = sa.select(Assignment.id).where(
                Assignment.volunteer_id.in_(volunteers_subquery)
            )
            shifts_subquery = sa.select(Assignment.shift_id).where(
                Assignment.volunteer_id.in_(volunteers_subquery)
            )
            assignements_stmt = sa.select(Assignment).where(
                sa.or_(
                    Assignment.volunteer_id.in_(volunteers_subquery),
                    Assignment.shift_id.in_(shifts_subquery),
                )
            )
            shifts_stmt = sa.select(Shift).where(Shift.id.in_(shifts_subquery))
            stations_subquery = sa.select(Shift.station_id).where(
                Shift.id.in_(shifts_subquery)
            )
            stations_stmt = (
                sa.select(Station, StationKind.kind)
                .join(
                    StationKind,
                    onclause=StationKind.label == Station.label,
                    isouter=True,
                )
                .where(Station.id.in_(stations_subquery))
            )
            volunteers_stmt = (
                sa.select(Volunteer, VolunteerStatus.arrived)
                .join(
                    VolunteerStatus,
                    onclause=VolunteerStatus.nivol == Volunteer.nivol,
                    isouter=True,
                )
                .where(
                    sa.or_(
                        Volunteer.dlus_email == user_email,
                        Volunteer.email == user_email,
                        Volunteer.id.in_(
                            sa.select(Assignment.volunteer_id).where(
                                Assignment.id.in_(assignements_subquery)
                            )
                        ),
                    )
                )
            )

        return {  # pyright: ignore[reportUnknownVariableType]
            "isSupervisor": is_supervisor,
            "isDlus": is_dlus,
            "myVolunteerId": session.execute(
                sa.select(Volunteer.id).where(Volunteer.email == user_email)
            ).scalar_one_or_none(),
            "volunteers": [
                {
                    "id": volunteer.id,
                    "firstname": volunteer.firstname,
                    "lastname": volunteer.lastname,
                    "nivol": volunteer.nivol,
                    "minor": volunteer.minor,
                    "mission_restrictions": volunteer.mission_restrictions,
                    "food_restrictions": volunteer.food_restrictions,
                    "incoming_date_time": volunteer.incoming_date_time,
                    "outgoing_date_time": volunteer.outgoing_date_time,
                    "department": volunteer.department,
                    "roles": volunteer.roles,
                    "dlus_email": volunteer.dlus_email,
                    "arrived": arrived,
                }
                for volunteer, arrived in session.execute(volunteers_stmt)
            ],
            "stations": [
                {
                    "id": station.id,
                    "label": station.label,
                    "kind": kind,
                }
                for station, kind in session.execute(stations_stmt)
            ],
            "shifts": (
                [
                    {
                        "id": shift.id,
                        "stationId": shift.station_id,
                        "startDateTime": shift.start_date_time,
                        "endDateTime": shift.end_date_time,
                        "meetDateTime": shift.meet_date_time,
                    }
                    for shift in session.execute(shifts_stmt).scalars()
                ]
            ),
            "assignments": (
                [
                    {
                        "id": assignment.id,
                        "shiftId": assignment.shift_id,
                        "volunteerId": assignment.volunteer_id,
                        "role": assignment.role,
                    }
                    for assignment in session.execute(assignements_stmt).scalars()
                ]
            ),
        }

    return data_inner()


@app.post("/uploadaffectation/")
async def create_upload_affectation(
    file: Annotated[
        UploadFile, File(description="Upload Affectation CSVs exported from Minos")
    ],
    _: str = Depends(verify_cf_authorization),
):
    @dbsession
    def upload_inner(session: so.Session):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.file.read())
        result = parse_affectations_csv(session=session, filename=Path(tfile.name))
        Path(tfile.name).unlink()
        return result

    return upload_inner()


@app.post("/uploadvolontaires/")
async def create_upload_volontaires(
    file: Annotated[
        UploadFile, File(description="Upload Volontaires CSVs exported from Minos")
    ],
    _: str = Depends(verify_cf_authorization),
):
    @dbsession
    def upload_inner(session: so.Session):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.file.read())
        result = parse_volontaires_csv(session=session, filename=Path(tfile.name))
        Path(tfile.name).unlink()
        return result

    return upload_inner()


class VolunteerStatusDTO(BaseModel):
    nivol: str
    arrived: bool | None = None


@app.post("/volunteer_status/")
async def set_volunteer_status(
    volunteer_status: VolunteerStatusDTO,
    _: str = Depends(verify_cf_authorization),
):
    @dbsession
    def set_volunteer_status_inner(session: so.Session):
        volunteer_status_in_db = session.execute(
            sa.select(VolunteerStatus).where(
                VolunteerStatus.nivol == volunteer_status.nivol
            )
        ).scalar_one_or_none()
        if not volunteer_status_in_db:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail="Unknown volunteer nivol"
            )
        volunteer_status_in_db.arrived = volunteer_status.arrived

    return set_volunteer_status_inner()


class StationKindDTO(BaseModel):
    label: str
    kind: str | None = None


@app.post("/station_kind/")
async def set_station_kind(
    station_kind: StationKindDTO,
    _: str = Depends(verify_cf_authorization),
):
    @dbsession
    def set_station_kind_inner(session: so.Session):
        station_kind_in_db = session.execute(
            sa.select(StationKind).where(StationKind.label == station_kind.label)
        ).scalar_one_or_none()
        if not station_kind_in_db:
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail="Unknown station label")
        station_kind_in_db.kind = station_kind.kind

    return set_station_kind_inner()


@app.delete("/data")
async def delete_all(
    _: str = Depends(verify_cf_authorization),
):

    @dbsession
    def delete_all_inner(session: so.Session):
        session.execute(sa.delete(Assignment))
        session.execute(sa.delete(Shift))
        session.execute(sa.delete(Station))
        session.execute(sa.delete(Volunteer))

    delete_all_inner()
