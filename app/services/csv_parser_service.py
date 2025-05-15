# app/services/csv_parser_service.py
import csv
import io
from typing import List, Dict
from .platform_config import platform_config
import difflib

def detect_platform(headers: List[str]) -> str:
    # Normalize headers to lower case and strip spaces
    normalized_headers = [h.strip().lower() for h in headers if h]

    for broker, cfg in platform_config.items():
        identifier = cfg["identifier"].strip().lower()
        if identifier in normalized_headers:
            return broker

    raise ValueError("Unknown CSV format.")

def normalize_csv(file_bytes: bytes) -> List[Dict]:
    text = file_bytes.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV file is missing headers.")

    print(f"🔍 Detected headers: {reader.fieldnames}")
    platform = detect_platform(list(reader.fieldnames or []))

    normalized = []
    for i, row in enumerate(reader):
        raw_cols = platform_config[platform]["columns"]
        cols = {}

        # Match platform_config keys to real CSV headers fuzzily
        for key, expected_header in raw_cols.items():
            best_match = difflib.get_close_matches(expected_header, reader.fieldnames or [], n=1, cutoff=0.6)
            if best_match:
                cols[key] = best_match[0]
            else:
                raise ValueError(f"Couldn't match column '{expected_header}' in {platform}")
        try:
            normalized.append({
                "symbol": row[cols["symbol"]],
                "quantity": float(row[cols["quantity"]]),
                "buy_price": float(row[cols["buy_price"]]),
                "current_price": float(row[cols["current_price"]]),
            })
        except Exception as e:
            print(f"Skipping row {i+1} in {platform}: {e}")
            continue

    print(f"Parsed {len(normalized)} valid rows from {platform}")
    return normalized

def compute_summary(all_trades: List[Dict]) -> Dict:
    total_invested = 0
    current_value = 0
    asset_map = {}

    for trade in all_trades:
        invested = trade["quantity"] * trade["buy_price"]
        current = trade["quantity"] * trade["current_price"]
        symbol = trade["symbol"]

        total_invested += invested
        current_value += current
        asset_map[symbol] = asset_map.get(symbol, 0) + current

    allocation = {
        sym: round((val / current_value) * 100, 2) for sym, val in asset_map.items()
    }

    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "total_profit": round(current_value - total_invested, 2),
        "asset_allocation": allocation,
    }