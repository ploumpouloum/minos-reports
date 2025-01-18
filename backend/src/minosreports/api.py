from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Upload CSVs exported from Minos")
    ],
):
    return {"files": [{"filenane": file.filename, "size": file.size} for file in files]}
