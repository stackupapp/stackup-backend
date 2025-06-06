from fastapi import APIRouter, Depends, Query
from app.utils.dependencies import get_current_user
from app.services.history_service import (
    get_portfolio_history,
    get_portfolio_trends,
)

router = APIRouter()

@router.get("/portfolio/history")
def history(
    username: str = Query(..., description="Username for retrieving history"),
    current_user: str = Depends(get_current_user)
):
    print(f"✅ Authenticated history request from: {current_user}")
    return {
        "history": get_portfolio_history(username)
    }



@router.get("/portfolio/trends")
def trends(
    username: str = Query(..., description="Username for retrieving trend data"),
    current_user: str = Depends(get_current_user)
):
    print(f"✅ Authenticated trends request from: {current_user}")
    return {
        "username": username,
        **get_portfolio_trends(username)
    }