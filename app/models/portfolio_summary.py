from pydantic import BaseModel
from typing import Dict

class StockDetails(BaseModel):
    quantity: float
    buy_price: float
    current_price: float
    current_value: float

class PortfolioSummary(BaseModel):
    total_invested: float
    current_value: float
    total_profit: float
    per_stock_details: Dict[str, StockDetails]
    asset_allocation: Dict[str, float]