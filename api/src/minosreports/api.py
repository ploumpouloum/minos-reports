import tempfile
from pathlib import Path
from typing import Annotated

import sqlalchemy as sa
import sqlalchemy.orm as so
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/data")
async def data():

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
async def delete_all():

    @dbsession
    def delete_all_inner(session: so.Session):
        session.execute(sa.delete(Assignment))
        session.execute(sa.delete(Shift))
        session.execute(sa.delete(Station))
        session.execute(sa.delete(Volunteer))

    delete_all_inner()
