import os
import uuid
from app.services.history_service import (
    save_portfolio_snapshot,
    get_portfolio_history,
    get_portfolio_trends,
)

def make_username():
    return f"testuser_{uuid.uuid4().hex[:6]}"

def cleanup_user_folder(username):
    folder = f"user_history/{username}"
    if os.path.exists(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        os.rmdir(folder)

def test_save_and_load_snapshot():
    username = make_username()
    cleanup_user_folder(username)

    snapshot = {
        "total_invested": 1000,
        "current_value": 1100,
        "total_profit": 100,
        "timestamp": "2024-01-01T00:00:00Z"
    }

    save_portfolio_snapshot(username, snapshot)
    history = get_portfolio_history(username)

    assert len(history) == 1
    assert history[0]["total_invested"] == 1000
    assert "timestamp" in history[0]

    cleanup_user_folder(username)

def test_portfolio_trends():
    username = make_username()
    cleanup_user_folder(username)

    snapshots = [
        {"total_invested": 1000, "current_value": 1100, "total_profit": 100, "timestamp": "2024-01-01T00:00:00Z"},
        {"total_invested": 1200, "current_value": 1150, "total_profit": -50, "timestamp": "2024-01-02T00:00:00Z"}
    ]

    for snap in snapshots:
        save_portfolio_snapshot(username, snap)

    trend_data = get_portfolio_trends(username)
    trends = trend_data["trends"]

    assert isinstance(trends, list)
    assert len(trends) == 2
    assert trends[0]["total_invested"] == 1000
    assert trends[1]["current_value"] == 1150

    cleanup_user_folder(username)