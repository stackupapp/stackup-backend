# app/services/csv_parser_service.py
import csv
import io
import difflib
from typing import List, Dict
from difflib import SequenceMatcher
from .finnhub_service import get_realtime_price
from app.services.finnhub_service import get_realtime_price

# Canonical header groups (no need for platform_config anymore)
FIELD_ALIASES = {
    "symbol": ["symbol", "ticker", "underlying symbol", "symbolname"],
    "quantity": ["quantity", "qty", "shares", "quantityheld"],
    "buy_price": ["buy", "entry", "cost basis", "average cost", "trade price", "t. price"],
    "current_price": ["current", "mark", "market value", "marketestimate", "market price"]
}

def fuzzy_header_mapping(headers: List[str]) -> Dict[str, str]:
    """Map CSV headers to canonical field keys based on fuzzy match."""
    mapped = {}
    headers_lower = [h.lower() for h in headers]

    for field_key, aliases in FIELD_ALIASES.items():
        best_match = ""
        best_score = 0
        for alias in aliases:
            for header in headers_lower:
                score = SequenceMatcher(None, alias, header).ratio()
                if score > best_score:
                    best_score = score
                    best_match = header
        # Map back to original casing
        for h in headers:
            if h.lower() == best_match:
                mapped[field_key] = h
                break

    return mapped

def normalize_csv(file_bytes: bytes) -> List[Dict]:
    """Parse a raw CSV and normalize trade data using fuzzy headers."""
    text = file_bytes.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV file is missing headers.")

    headers = list(reader.fieldnames)
    print(f"Detected headers: {headers}")

    cols = fuzzy_header_mapping(headers)

    # Ensure all required fields are present
    required_keys = ["symbol", "quantity", "buy_price", "current_price"]
    for key in required_keys:
        if key not in cols:
            raise ValueError(f"Couldn't map required column: {key}")

    normalized = []
    for i, row in enumerate(reader):
        try:
            normalized.append({
                "symbol": row[cols["symbol"]],
                "quantity": float(row[cols["quantity"]]),
                "buy_price": float(row[cols["buy_price"]]),
                "current_price": float(row[cols["current_price"]]),
            })
        except Exception as e:
            print(f"Skipping row {i+1}: {e}")
            continue

    print(f"Parsed {len(normalized)} valid rows")
    return normalized

def compute_summary(all_trades: List[Dict]) -> Dict:
    total_invested = 0
    current_value = 0
    asset_map = {}
    per_stock_details = {}

    for trade in all_trades:
        symbol = trade["symbol"]
        quantity = trade["quantity"]
        buy_price = trade["buy_price"]

        try:
            # Fetch real-time current price
            current_price = get_realtime_price(symbol)
        except Exception as e:
            print(f"⚠️ Could not fetch price for {symbol}: {e}")
            current_price = trade["current_price"]  # fallback to file value

        invested = quantity * buy_price
        current = quantity * current_price

        total_invested += invested
        current_value += current
        asset_map[symbol] = asset_map.get(symbol, 0) + current

        # Store per-stock breakdown
        per_stock_details[symbol] = {
            "quantity": quantity,
            "buy_price": buy_price,
            "current_price": round(current_price, 2),
            "current_value": round(current, 2),
        }

    allocation = {
        sym: round((val / current_value) * 100, 2)
        for sym, val in asset_map.items()
    }

    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "total_profit": round(current_value - total_invested, 2),
        "per_stock_details": per_stock_details,
        "asset_allocation": allocation,
    }