import csv
import time
from functools import cache, wraps
from typing import Any, Callable, Generator

from performance_tools import measure_performance


def load_sales(path: str) -> Generator[dict[str, str], None, None]:
    """Stream sales data lazily from disk."""
    print("Streaming CSV data lazily...")
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


# --- Custom TTL (Time-To-Live) cache decorator ---
def ttl_cache(seconds: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A simple time-limited cache decorator."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache_data = {}
        cache_time = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            current_time = time.time()

            # Check if cached and still valid
            if key in cache_data and (current_time - cache_time[key]) < seconds:
                return cache_data[key]

            # Otherwise, recompute and cache it
            result = func(*args, **kwargs)
            cache_data[key] = result
            cache_time[key] = current_time
            return result

        return wrapper

    return decorator


@ttl_cache(seconds=60)
def get_conversion_rates() -> dict[str, float]:
    """Simulate fetching conversion rates, cached for 60 seconds."""
    print("Fetching conversion rates from remote service...")
    time.sleep(2)  # Simulate API delay
    return {"USD": 1.0, "EUR": 1.1, "JPY": 0.007}


@cache
def compute_total_sales(path: str) -> float:
    """Compute total sales and cache the numeric result."""
    print("Calculating total sales (this may take a while)...")
    return sum(float(s["amount"]) for s in load_sales(path))


@cache
def compute_sales_count(path: str) -> int:
    """Compute and cache total record count."""
    print("Counting total sales records (this may take a while)...")
    return sum(1 for _ in load_sales(path))


@measure_performance
def analyse_sales(path: str, currency: str) -> float:
    """Compute total converted sales and return result."""
    total = compute_total_sales(path)
    rate = get_conversion_rates().get(currency, 1.0)
    return total * rate


@measure_performance
def count_sales(path: str) -> int:
    """Compute and return the total number of sales."""
    return compute_sales_count(path)


def main() -> None:
    path = "sales.csv"

    while True:
        print("\nChoose an option:")
        print("1. Analyse sales data")
        print("2. Count total sales records")
        print("3. Quit")

        choice = input("> ")

        if choice == "1":
            currency = input("Enter currency (USD/EUR/JPY): ").upper() or "USD"
            converted_total = analyse_sales(path, currency)
            print(f"Total sales in {currency}: {converted_total:.2f}")

        elif choice == "2":
            count = count_sales(path)
            print(f"Number of sales: {count:,}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
