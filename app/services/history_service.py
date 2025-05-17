import os
import json
from typing import Dict
from datetime import datetime

# Define folder path
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_portfolio_snapshot(username: str, summary: dict):
    file_path = os.path.join(DATA_DIR, f"{username}_history.json")
    print(f"Saving history for user: {username} → {file_path}")

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        from datetime import datetime
        data.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",  # UTC time
            **summary
        })

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        print("History saved successfully.")
    except Exception as e:
        print(f"Error saving history: {e}")

def get_portfolio_history(username: str) -> list:
    file_path = os.path.join(DATA_DIR, f"{username}_history.json")
    print(f"Loading history from: {file_path}")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# app/services/history_service.py

def get_portfolio_trends(username: str) -> Dict:
    file_path = os.path.join(DATA_DIR, f"{username}_history.json")
    print(f"📈 Loading trends from: {file_path}")

    if not os.path.exists(file_path):
        return {"trends": []}

    with open(file_path, "r") as f:
        data = json.load(f)

    # Filter entries that have timestamp and investment data
    trends = []
    for entry in data:
        try:
            trends.append({
                "timestamp": entry["timestamp"],
                "total_invested": entry["total_invested"],
                "current_value": entry["current_value"],
                "total_profit": round(entry["current_value"] - entry["total_invested"], 2)
            })
        except KeyError as e:
            print(f"⚠️ Skipping entry due to missing key: {e}")

    # Sort by timestamp
    trends = sorted(trends, key=lambda x: datetime.fromisoformat(x["timestamp"].replace("Z", "+00:00")))

    return {"trends": trends}