from functools import cache
from time import sleep

from cachetools import TTLCache, cached


@cache
def exchange_rate(currency: str) -> float:
    """Convenient, but this cached value never expires."""
    print(f"Fetching {currency} rate")
    return 1.08


ttl_cache: TTLCache[str, float] = TTLCache(maxsize=100, ttl=60)


@cached(ttl_cache)
def fresh_exchange_rate(currency: str) -> float:
    """Bounded cache with an expiry policy that matches volatile data."""
    print(f"Fetching {currency} rate")
    return 1.08


def main() -> None:
    print(exchange_rate("EUR"))
    print(exchange_rate("EUR"))  # No second fetch; it may now be stale.
    print(exchange_rate.cache_info())

    print(fresh_exchange_rate("EUR"))
    sleep(0.01)
    print(fresh_exchange_rate("EUR"))  # Cached for at most 60 seconds.
    print(f"TTL cache contains {len(ttl_cache)} item(s)")


if __name__ == "__main__":
    main()
