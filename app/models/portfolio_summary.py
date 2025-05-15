from pydantic import BaseModel
from typing import Dict

class PortfolioSummary(BaseModel):
    total_invested: float
    current_value: float
    total_profit: float
    asset_allocation: Dict[str, float]  