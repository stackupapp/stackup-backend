# app/models/history.py
from typing import List, Dict
from pydantic import BaseModel

class PerStockDetail(BaseModel):
    quantity: float
    buy_price: float
    current_price: float
    current_value: float

class HistorySnapshot(BaseModel):
    timestamp: str
    total_invested: float
    current_value: float
    total_profit: float
    per_stock_details: Dict[str, PerStockDetail]
    asset_allocation: Dict[str, float]

class HistoryResponse(BaseModel):
    history: List[HistorySnapshot]

class TrendPoint(BaseModel):
    timestamp: str
    total_invested: float
    current_value: float
    total_profit: float

class TrendsResponse(BaseModel):
    trends: List[TrendPoint]