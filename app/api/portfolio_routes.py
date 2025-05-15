# app/api/portfolio_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models.portfolio_summary import PortfolioSummary
from app.services.csv_parser_service import normalize_csv, compute_summary

router = APIRouter()

@router.post("/portfolio/upload", response_model=PortfolioSummary)
async def upload_portfolio(files: List[UploadFile] = File(...)):
    all_trades = []

    for file in files:
        print(f"Processing file: {file.filename}")
        if not file.filename or not file.filename.endswith(".csv"):
            print("Skipping non-CSV file")
            continue

        try:
            content = await file.read()
            parsed = normalize_csv(content)
            print(f"Parsed {len(parsed)} trades from {file.filename}")
            all_trades.extend(parsed)
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue

    if not all_trades:
        raise HTTPException(status_code=400, detail="No valid trade data found.")

    summary = compute_summary(all_trades)
    return summary