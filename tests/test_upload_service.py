import pytest
from unittest.mock import patch
from app.services.upload_service import parse_and_save

def test_parse_and_save_valid():
    username = "testuser"
    fake_csv = b"Symbol,Quantity,Buy Price,Current Price\nAAPL,10,150,155"

    # Patch where get_realtime_price is actually used
    with patch("app.services.csv_parser_service.get_realtime_price", return_value=155.0):
        summary = parse_and_save(username, fake_csv)

    assert summary["total_invested"] == 1500
    assert summary["current_value"] == 1550

def test_parse_and_save_empty_csv():
    username = "testuser"
    fake_csv = b""  # empty bytes

    with pytest.raises(ValueError, match="CSV file is missing headers."):
        parse_and_save(username, fake_csv)

def test_parse_and_save_missing_headers():
    username = "testuser"
    fake_csv = b"Foo,Bar,Baz\nAAPL,10,150"  # These won't match anything

    with pytest.raises(ValueError, match="Couldn't map required column"):
        parse_and_save(username, fake_csv)

def test_parse_and_save_malformed_row():
    username = "testuser"
    fake_csv = b"Symbol,Quantity,Buy Price,Current Price\nAAPL,ten,150,155"

    with patch("app.services.csv_parser_service.get_realtime_price", return_value=155.0):
        summary = parse_and_save(username, fake_csv)

    # Should skip invalid row, result in 0 values
    assert summary["total_invested"] == 0
    assert summary["current_value"] == 0
    assert summary["total_profit"] == 0

