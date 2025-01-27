import sqlalchemy.orm as so
import sqlalchemy as sa
from pathlib import Path
import tempfile
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import csv
import datetime

from minosreports.db import dbsession
from minosreports.db.models import Shift, Station, Volunteer, Assignment

app = FastAPI()

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
    def data_inner(session: so.Session):
        return {
            "volunteers": [
                {
                    "id": volunteer.id,
                    "firstname": volunteer.firstname,
                    "lastname": volunteer.lastname,
                } for volunteer in session.execute(sa.select(Volunteer)).scalars()
            ], 
            "stations": [
                {
                    "id": station.id,
                    "label": station.label,
                } for station in session.execute(sa.select(Station)).scalars()
            ], 
            "shifts": [
                {
                    "id": shift.id,
                    "stationId": shift.station_id,
                    "startDateTime": shift.startDateTime,
                    "endDateTime": shift.endDateTime,
                } for shift in session.execute(sa.select(Shift)).scalars()
            ], 
            "assignments": [
                {
                    "id": assignment.id,
                    "shiftId": assignment.shift_id,
                    "volunteerId": assignment.volunteer_id,
                    "role": assignment.role,
                } for assignment in session.execute(sa.select(Assignment)).scalars()
            ]
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
        session.execute(sa.delete(Assignment))
        session.execute(sa.delete(Shift))
        session.execute(sa.delete(Station))
        session.execute(sa.delete(Volunteer))
        countRows: int = 0
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.file.read())
        with open(tfile.name, encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                if row["Volontaire"].strip():
                    volunteer = get_volunteer(row["Volontaire"])
                    stmt = sa.select(Volunteer).where(Volunteer.firstname == volunteer.firstname).where(Volunteer.lastname == volunteer.lastname)
                    volunteer_in_db = session.execute(stmt).scalar_one_or_none()
                    if volunteer_in_db is None:
                        print(f"Adding volunteer {volunteer.firstname} {volunteer.lastname}")
                        session.add(volunteer)
                        volunteer_in_db = session.execute(stmt).scalar_one()
                else:
                    volunteer_in_db = None

                bad_row = False
                for field in ["Nom DPS", "Date", "Début de poste", "Fin de poste", "Qualification"]:
                    if not row[field].strip():
                        print(f"Ignoring line without '{field}'")
                        bad_row = True
                        break
                if bad_row:
                    continue

                station = get_station(nom_dps=row["Nom DPS"])
                stmt = sa.select(Station).where(Station.label == station.label)
                station_in_db = session.execute(stmt).scalar_one_or_none()
                if station_in_db is None:
                    print(f"Adding station {station.label}")
                    session.add(station)
                    station_in_db = session.execute(stmt).scalar_one()

                shift = get_shift(station=station_in_db, date=row["Date"], debut_de_poste=row["Début de poste"], fin_de_poste=row["Fin de poste"])
                stmt = sa.select(Shift).where(Shift.station == shift.station).where(Shift.startDateTime == shift.startDateTime).where(Shift.endDateTime == shift.endDateTime)
                shift_in_db = session.execute(stmt).scalar_one_or_none()
                if shift_in_db is None:
                    print(f"Adding shift from {shift.startDateTime} to {shift.endDateTime} for {shift.station.label}")
                    session.add(shift)
                    shift_in_db = session.execute(stmt).scalar_one()

                assignment = Assignment(role=row["Qualification"])
                assignment.shift = shift_in_db
                assignment.volunteer = volunteer_in_db
                print(f"Adding assignment of {assignment.volunteer.firstname if assignment.volunteer else 'Nobody'} {assignment.volunteer.lastname if assignment.volunteer else ''} as {assignment.role} for {assignment.shift.station.label} from {assignment.shift.startDateTime} to {assignment.shift.endDateTime}")
                session.add(assignment)


        Path(tfile.name).unlink()
        return {"countRows": countRows}
    
    return upload_inner()

def get_volunteer(value: str) -> Volunteer:
    splits = value.split(" ")
    return Volunteer(firstname= splits[1] if len(splits) > 1 else "", lastname=splits[0])

def get_station(nom_dps: str) -> Station:
    return Station(label=nom_dps)

def get_shift(station: Station, date: str, debut_de_poste: str, fin_de_poste: str) -> Shift:
    date_splits = [int(value) for value in date.split("/")]
    debut_splits = [int(value) for value in debut_de_poste.split(":")]
    fin_splits = [int(value) for value in fin_de_poste.split(":")]
    
    start_day = datetime.datetime(day=date_splits[0], month=date_splits[1], year=date_splits[2], hour=debut_splits[0], minute=debut_splits[1])
    end_day = datetime.datetime(day=date_splits[0], month=date_splits[1], year=date_splits[2], hour=fin_splits[0], minute=fin_splits[1])
    if end_day < start_day:
        end_day += datetime.timedelta(days=1)
    shift = Shift(startDateTime=start_day, endDateTime=end_day)
    shift.station = station
    return shift
