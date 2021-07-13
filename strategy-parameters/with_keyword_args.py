"""
Basic example of a Trading bot with a strategy pattern.
"""
from abc import ABC, abstractmethod

from exchange import Exchange


class TradingStrategy(ABC):
    """Trading strategy that decides whether to buy or sell, given a list of prices."""

    @abstractmethod
    def should_buy(self, prices: list[float], **kwargs: float) -> bool:
        """Whether you should buy this coin, given the prices."""

    @abstractmethod
    def should_sell(self, prices: list[float], **kwargs: float) -> bool:
        """Whether you should sell this coin, given the prices."""


class AverageTradingStrategy(TradingStrategy):
    """Trading strategy based on price averages."""

    def should_buy(self, prices: list[float], **kwargs: float) -> bool:
        window_size = kwargs.get("window_size", 3.0)
        list_window = prices[-int(window_size) :]
        return prices[-1] < sum(list_window) / len(list_window)

    def should_sell(self, prices: list[float], **kwargs: float) -> bool:
        window_size = kwargs.get("window_size", 3.0)
        list_window = prices[-int(window_size) :]
        return prices[-1] > sum(list_window) / len(list_window)


class MinMaxTradingStrategy(TradingStrategy):
    """Trading strategy based on price minima and maxima."""

    def should_buy(self, prices: list[float], **kwargs: float) -> bool:
        # buy if it's below the min_price
        return prices[-1] < kwargs.get("min_price", 32000.0)

    def should_sell(self, prices: list[float], **kwargs: float) -> bool:
        # sell if it's above $33,000
        return prices[-1] > kwargs.get("max_price", 33000.0)


class TradingBot:
    """Trading bot that connects to a crypto exchange and performs trades."""

    def __init__(self) -> None:
        self.exchange = Exchange()
        self.exchange.connect()

    def run(self, coin: str, trading_strategy: TradingStrategy):
        """Run the trading bot once for a particular coin, with a given strategy."""
        prices = self.exchange.get_market_data(coin)
        should_buy = trading_strategy.should_buy(prices, min_price=31000)
        should_sell = trading_strategy.should_sell(prices, max_price=33000)
        if should_buy:
            self.exchange.buy(coin, 10)
        elif should_sell:
            self.exchange.sell(coin, 10)
        else:
            print(f"No action needed for {coin}.")


def main() -> None:
    """Main function."""

    bot = TradingBot()
    bot.run("BTC/USD", MinMaxTradingStrategy())


if __name__ == "__main__":
    main()
