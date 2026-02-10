from langchain_core.tools import tool


@tool
def get_stock_price(symbol: str) -> float:
    """Return the current price of a stock."""
    prices = {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6,
    }
    return prices.get(symbol.upper(), 0.0)


@tool
def prepare_buy(symbol: str, quantity: int, total_price: float) -> str:
    """Prepare a buy request. Human approval is handled by the graph."""
    return f"REQUEST_BUY::{symbol}::{quantity}::{total_price}"
