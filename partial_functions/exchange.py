from dataclasses import dataclass
from decimal import Decimal


class ExchangeConnectionError(Exception):
    """Custom error that is raised when an exchange is not connected."""


@dataclass
class Exchange:
    connected: bool = False

    def connect(self) -> None:
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def check_connection(self) -> None:
        """Check if the exchange is connected."""
        if not self.connected:
            raise ExchangeConnectionError()

    def get_market_data(self, symbol: str) -> list[int]:
        """Return fake market price data for a given market symbol."""
        self.check_connection()

        price_data = {
            "BTC/USD": [
                35_842_00,
                34_069_00,
                33_871_00,
                34_209_00,
                32_917_00,
                33_931_00,
                33_370_00,
                34_445_00,
                32_901_00,
                33_013_00,
            ],
            "ETH/USD": [
                2_381_00,
                2_233_00,
                2_300_00,
                2_342_00,
                2_137_00,
                2_156_00,
                2_103_00,
                2_165_00,
                2_028_00,
                2_004_00,
            ],
        }
        return price_data[symbol]

    def buy(self, symbol: str, amount: int) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")
