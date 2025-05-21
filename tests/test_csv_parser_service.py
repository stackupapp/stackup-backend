import pytest
from app.services.csv_parser_service import normalize_csv

def test_normalize_csv_headers():
    sample_csv = b"Symbol,Quantity,Buy Price,Current Price\nAAPL,10,150.0,155.0\nTSLA,5,700.0,705.0"

    result = normalize_csv(sample_csv)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["symbol"] == "AAPL"
    assert result[0]["quantity"] == 10
    assert result[0]["buy_price"] == 150.0
    assert result[0]["current_price"] == 155.0