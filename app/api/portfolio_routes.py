# app/api/portfolio_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List
from app.models.portfolio_summary import PortfolioSummary
from app.services.csv_parser_service import normalize_csv, compute_summary
from app.services.history_service import save_portfolio_snapshot, get_portfolio_history
from app.services.history_service import get_portfolio_trends
from app.models.history import HistoryResponse
from fastapi import Depends
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/portfolio/upload", response_model=PortfolioSummary,
             openapi_extra={"security": [{"BearerAuth": []}]})
async def upload_portfolio(
    files: List[UploadFile] = File(...),
    username: str = Query(..., description="Username for saving snapshot"),
    current_user: str = Depends(get_current_user)
):
    print(f"✅ Authenticated upload request from: {current_user}")
    
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

    # TEMPORARY: Accept username as a query param (you'll secure this later)
    summary = compute_summary(all_trades)

    # Save snapshot to disk
    save_portfolio_snapshot(username=username, summary=summary)
    return summary

@router.get("/portfolio/history", response_model=HistoryResponse)
def view_history(username: str):
    """
    Returns a list of historical portfolio snapshots for the given user.
    """
    try:
        history = get_portfolio_history(username)
        print(f"Loaded history for {username}: {len(history)} entries")
        return {"history": history}
    except Exception as e:
        import traceback
        print(f"Error loading history: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# app/api/portfolio_routes.py

@router.get("/portfolio/trends")
def view_trends(username: str):
    """
    Returns investment trends over time for the given user.
    """
    try:
        return get_portfolio_trends(username)
    except Exception as e:
        return {"error": str(e)}
