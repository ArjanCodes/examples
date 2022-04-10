import statistics
from dataclasses import dataclass
from typing import Callable

TradingStrategyFunction = Callable[[list[int]], bool]


@dataclass
class TradingBot:

    buy_strategy: TradingStrategyFunction
    sell_strategy: TradingStrategyFunction

    def run(self, prices: list[int]) -> None:
        if self.buy_strategy(prices):
            print("Buy!")
        elif self.sell_strategy(prices):
            print("Sell!")
        else:
            print("No action needed.")


def should_buy_avg(prices: list[int]) -> bool:
    list_window = prices[-3:]
    return prices[-1] < statistics.mean(list_window)


def should_buy_minmax(prices: list[int]) -> bool:
    return prices[-1] < 32_000_00


def should_sell_avg(prices: list[int]) -> bool:
    list_window = prices[-3:]
    return prices[-1] > statistics.mean(list_window)


def should_sell_minmax(prices: list[int]) -> bool:
    return prices[-1] > 33_000_00


def main() -> None:
    bot = TradingBot(should_buy_minmax, should_sell_minmax)
    bot.run(
        [
            32_917_00,
            33_931_00,
            33_370_00,
            34_445_00,
            32_901_00,
            33_013_00,
        ]
    )


if __name__ == "__main__":
    main()
