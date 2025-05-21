# app/services/upload_service.py
import os
from typing import Tuple
from fastapi import UploadFile
from app.services.finnhub_service import get_realtime_price
from app.services.csv_parser_service import normalize_csv, compute_summary
from app.services.history_service import save_portfolio_snapshot

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(file: UploadFile) -> Tuple[str, int]:
    filename = file.filename or "unknown_file"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = file.file.read()  # Read content
        f.write(content)

    return filename, len(content)

def parse_and_save(username: str, file_bytes: bytes) -> dict:
    """
    Parses a raw CSV, calculates the summary, and saves the snapshot for history.
    """
    # Parse & normalize trades
    trades = normalize_csv(file_bytes)

    # Calculate summary from trades
    summary = compute_summary(trades)

    # Save snapshot
    save_portfolio_snapshot(username, summary)

    return summary