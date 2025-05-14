# app/api/upload_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.upload_service import save_upload_file
from app.models.upload_response import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file was uploaded.")
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    filename, size = save_upload_file(file)
    return UploadResponse(filename=filename, size=size)