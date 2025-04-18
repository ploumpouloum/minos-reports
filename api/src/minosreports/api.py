import tempfile
from http import HTTPStatus
from pathlib import Path
from typing import Annotated

import sqlalchemy as sa
import sqlalchemy.orm as so
from fastapi import Cookie, Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from minosreports.cloudflare_access import InvalidTokenError, verify_token
from minosreports.context import Context
from minosreports.db import dbsession
from minosreports.db.models import Assignment, Shift, Station, Volunteer
from minosreports.parsing.affectations import parse_affectations_csv
from minosreports.parsing.volontaires import parse_volontaires_csv

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

    if user_email not in context.supervisor_mails + context.dlus_mails:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    @dbsession
    def data_inner(session: so.Session):  # pyright: ignore[reportUnknownParameterType]
        return {  # pyright: ignore[reportUnknownVariableType]
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
                    "roles": volunteer.roles,
                }
                for volunteer in session.execute(sa.select(Volunteer)).scalars()
            ],
            "stations": [
                {
                    "id": station.id,
                    "label": station.label,
                }
                for station in session.execute(sa.select(Station)).scalars()
            ],
            "shifts": [
                {
                    "id": shift.id,
                    "stationId": shift.station_id,
                    "startDateTime": shift.start_date_time,
                    "endDateTime": shift.end_date_time,
                    "meetDateTime": shift.meet_date_time,
                }
                for shift in session.execute(sa.select(Shift)).scalars()
            ],
            "assignments": [
                {
                    "id": assignment.id,
                    "shiftId": assignment.shift_id,
                    "volunteerId": assignment.volunteer_id,
                    "role": assignment.role,
                }
                for assignment in session.execute(sa.select(Assignment)).scalars()
            ],
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
