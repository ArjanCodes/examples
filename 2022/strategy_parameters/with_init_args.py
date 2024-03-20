"""
Basic example of a Trading bot with a strategy pattern.
"""

import statistics
from abc import ABC, abstractmethod
from dataclasses import dataclass

from exchange import Exchange


class TradingStrategy(ABC):
    """Trading strategy that decides whether to buy or sell, given a list of prices."""

    @abstractmethod
    def should_buy(self, prices: list[float]) -> bool:
        """Whether you should buy this coin, given the prices."""

    @abstractmethod
    def should_sell(self, prices: list[float]) -> bool:
        """Whether you should sell this coin, given the prices."""


@dataclass
class AverageTradingStrategy(TradingStrategy):
    """Trading strategy based on price averages."""

    window_size: int = 3

    def should_buy(self, prices: list[float]) -> bool:
        list_window = prices[-int(self.window_size) :]
        return prices[-1] < statistics.mean(list_window)

    def should_sell(self, prices: list[float]) -> bool:
        list_window = prices[-int(self.window_size) :]
        return prices[-1] > statistics.mean(list_window)


@dataclass
class MinMaxTradingStrategy(TradingStrategy):
    """Trading strategy based on price minima and maxima."""

    min_price: float = 32000.0
    max_price: float = 33000.0

    def should_buy(self, prices: list[float]) -> bool:
        # buy if it's below the min_price
        return prices[-1] < self.min_price

    def should_sell(self, prices: list[float]) -> bool:
        # sell if it's above $33,000
        return prices[-1] > self.max_price


class TradingBot:
    """Trading bot that connects to a crypto exchange and performs trades."""

    def __init__(self, exchange: Exchange, trading_strategy: TradingStrategy) -> None:
        self.exchange = exchange
        self.trading_strategy = trading_strategy

    def run(self, symbol: str):
        """Run the trading bot once for a particular symbol, with a given strategy."""
        prices = self.exchange.get_market_data(symbol)
        should_buy = self.trading_strategy.should_buy(prices)
        should_sell = self.trading_strategy.should_sell(prices)
        if should_buy:
            self.exchange.buy(symbol, 10)
        elif should_sell:
            self.exchange.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")


def main() -> None:
    """
    Create an exchange and a trading bot with a strategy.
    Run the strategy once on a particular symbol.
    """

    # create the exchange and connect to it
    exchange = Exchange()
    exchange.connect()

    # create the trading strategy
    trading_strategy = MinMaxTradingStrategy(min_price=31000, max_price=34000)

    # create the trading bot and run the bot once
    bot = TradingBot(exchange, trading_strategy)
    bot.run("BTC/USD")


if __name__ == "__main__":
    main()
