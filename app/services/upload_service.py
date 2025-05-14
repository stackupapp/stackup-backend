# app/services/upload_service.py
import os
from fastapi import UploadFile
from typing import Tuple

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(file: UploadFile) -> Tuple[str, int]:
    filename = file.filename or "unknown_file"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = file.file.read()  # Read content
        f.write(content)

    return filename, len(content)