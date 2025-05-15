platform_config = {
    "Robinhood": {
        "identifier": "Symbol",
        "columns": {
            "symbol": "Symbol",
            "quantity": "Quantity",
            "buy_price": "Cost Basis",
            "current_price": "Market Value"
        }
    },
    "tos": {
        "identifier": "Open Date",  # Haven't tested this file yet
        "columns": {
            "symbol": "Underlying Symbol",
            "quantity": "Qty",
            "buy_price": "Trade Price",
            "current_price": "Mark"
        }
    },
    "IBKR": {
        "identifier": "Symbol",
        "columns": {
            "symbol": "Symbol",
            "quantity": "Quantity",
            "buy_price": "T. Price",  # use exact from header
            "current_price": "Market Price"
        }
    }
}