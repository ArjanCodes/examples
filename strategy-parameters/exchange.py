"""
Simple module that simulates an exchange.
"""


class ExchangeConnectionError(Exception):
    """Custom error that is raised when an exchange is not connected."""


class Exchange:
    """Basic exchange simulator."""

    def __init__(self):
        self.connected = False

    def connect(self):
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def get_market_data(self, coin: str) -> list[float]:
        """Returns fake market price data for a given coin."""
        if not self.connected:
            raise ExchangeConnectionError()

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
        return price_data[coin]

    def buy(self, coin: str, amount: float):
        """Simulates buying an amount of a given coin at the current price."""
        if not self.connected:
            raise ExchangeConnectionError()
        print(f"Buying amount {amount} of {coin}.")

    def sell(self, coin: str, amount: float):
        """Simulates selling an amount of a given coin at the current price."""
        if not self.connected:
            raise ExchangeConnectionError()
        print(f"Selling amount {amount} of {coin}.")
