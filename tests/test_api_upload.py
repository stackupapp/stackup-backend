import io
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def make_csv_file():
    content = (
        "Symbol,Quantity,Buy Price,Current Price\n"
        "AAPL,10,150.0,155.0\n"
        "TSLA,5,700.0,705.0"
    )
    return io.BytesIO(content.encode("utf-8"))

def test_upload_portfolio_success():
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    csv_file = make_csv_file()

    response = client.post(
        f"/portfolio/upload?username={username}",
        files={"files": ("portfolio.csv", csv_file, "text/csv")},
    )

    assert response.status_code == 200
    data = response.json()

    assert "total_invested" in data
    assert "current_value" in data
    assert "total_profit" in data
    assert data["total_invested"] > 0
    assert data["current_value"] > 0

def test_portfolio_history():
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    csv_file = make_csv_file()

    # Upload CSV to generate history
    response = client.post(
        f"/portfolio/upload?username={username}",
        files={"files": ("portfolio.csv", csv_file, "text/csv")},
    )
    assert response.status_code == 200

    # Fetch history
    hist_response = client.get(f"/portfolio/history?username={username}")
    assert hist_response.status_code == 200
    history = hist_response.json()["history"]

    assert isinstance(history, list)
    assert len(history) >= 1
    assert "total_invested" in history[0]
    assert "timestamp" in history[0]

def test_portfolio_trends():
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    csv_file = make_csv_file()

    # Upload twice to generate multiple snapshots
    for _ in range(2):
        response = client.post(
            f"/portfolio/upload?username={username}",
            files={"files": ("portfolio.csv", csv_file, "text/csv")},
        )
        assert response.status_code == 200

    # Fetch trend data
    trend_response = client.get(f"/portfolio/trends?username={username}")
    assert trend_response.status_code == 200

    trend_data = trend_response.json()
    assert "trends" in trend_data
    trends = trend_data["trends"]

    assert isinstance(trends, list)
    assert len(trends) >= 2
    assert "total_invested" in trends[0]
    assert "current_value" in trends[1]
    assert "timestamp" in trends[1]

def test_upload_missing_file():
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    response = client.post(
        f"/portfolio/upload?username={username}",
        files={}  # No file provided
    )
    assert response.status_code == 422  # FastAPI's unprocessable entity