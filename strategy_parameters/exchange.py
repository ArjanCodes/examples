"""
Simple module that simulates an exchange.
"""


class ExchangeConnectionError(Exception):
    """Custom error that is raised when an exchange is not connected."""


class Exchange:
    """Basic exchange simulator."""

    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> None:
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def check_connection(self) -> None:
        """Check if the exchange is connected."""
        if not self.connected:
            raise ExchangeConnectionError()

    def get_market_data(self, symbol: str) -> list[float]:
        """Return fake market price data for a given market symbol."""
        self.check_connection()

        price_data = {
            "BTC/USD": [
                35842.0,
                34069.0,
                33871.0,
                34209.0,
                32917.0,
                33931.0,
                33370.0,
                34445.0,
                32901.0,
                33013.0,
            ],
            "ETH/USD": [
                2381.0,
                2233.0,
                2300.0,
                2342.0,
                2137.0,
                2156.0,
                2103.0,
                2165.0,
                2028.0,
                2004.0,
            ],
        }
        return price_data[symbol]

    def buy(self, symbol: str, amount: float) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: float) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")
