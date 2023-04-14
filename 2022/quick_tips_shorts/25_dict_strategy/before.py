import statistics


def should_buy_avg(prices: list[int]) -> bool:
    list_window = prices[-3:]
    return prices[-1] < statistics.mean(list_window)


def should_buy_minmax(prices: list[int]) -> bool:
    return prices[-1] < 32_000_00


def should_buy_price_drop(prices: list[int]) -> bool:
    return prices[-1] < prices[-2]


def should_buy(prices: list[int], strategy: str) -> bool:
    if strategy == "avg":
        return should_buy_avg(prices)
    elif strategy == "minmax":
        return should_buy_minmax(prices)
    elif strategy == "price_drop":
        return should_buy_price_drop(prices)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def main() -> None:
    prices = [
        32_917_00,
        33_931_00,
        33_370_00,
        34_445_00,
        32_901_00,
        33_013_00,
    ]
    print(f"Should buy: {should_buy(prices, 'price_drop')}")


if __name__ == "__main__":
    main()
