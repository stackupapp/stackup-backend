# app/services/finnhub_service.py
import os
import requests

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1/quote"

def get_realtime_price(symbol: str) -> float:
    """Fetch real-time stock price for a given symbol from Finnhub."""
    if not FINNHUB_API_KEY:
        raise RuntimeError("FINNHUB_API_KEY is not set in environment")

    response = requests.get(BASE_URL, params={"symbol": symbol, "token": FINNHUB_API_KEY})
    if response.status_code != 200:
        raise RuntimeError(f"Finnhub API error: {response.status_code} - {response.text}")

    data = response.json()
    return data.get("c")  # 'c' is the current price in Finnhub's response