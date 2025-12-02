import json
import os
from typing import Any, Sequence


# No dataclasses, no immutability
class Sale:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency
        self.converted: float | None = None


# -------------------------------------------------------------------
# Expensive CSV parsing (NO caching)
# -------------------------------------------------------------------


def total_from_file(path: str) -> float:
    """Compute total sales by reading and parsing a large CSV file."""
    print(f"Reading file: {path}")
    total = 0.0
    with open(path) as f:
        for line in f:
            _, amount = line.strip().split(",")
            total += float(amount)
    return total


# -------------------------------------------------------------------
# NO protocols — duck typing
# -------------------------------------------------------------------


class StaticRateFetcher:
    def get_rate(self, currency: str) -> float:
        rates = {"EUR": 1.1, "USD": 1.0}
        return rates.get(currency, 1.0)


# Mutation instead of replace()
def convert_sale(sale: Sale, fetcher: StaticRateFetcher) -> Sale:
    rate = fetcher.get_rate(sale.currency)
    sale.converted = sale.amount * rate
    return sale


# -------------------------------------------------------------------
# Manual adjacent iteration (NO itertools.pairwise)
# -------------------------------------------------------------------


def compute_sales_deltas(numbers: Sequence[float]) -> list[float]:
    deltas: list[float] = []
    for i in range(len(numbers) - 1):
        deltas.append(numbers[i + 1] - numbers[i])
    return deltas


# -------------------------------------------------------------------
# Assignment expression BEFORE: manual double-read
# -------------------------------------------------------------------


def read_large_file(path: str) -> int:
    total = 0
    f = open(path, "rb")
    chunk = f.read(4096)
    while chunk:
        total += len(chunk)
        chunk = f.read(4096)
    f.close()
    return total


# -------------------------------------------------------------------
# BEFORE: No suppress, no pathlib file iteration
# -------------------------------------------------------------------


def load_all_json(directory: str) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(directory, filename)) as f:
                results[filename[:-5]] = json.load(f)
        except Exception:
            pass  # fallback
    return results


# -------------------------------------------------------------------
# Demo
# -------------------------------------------------------------------


def main() -> None:
    print("\n--- Caching Demo (Before) ---")
    print(total_from_file("sales_2025_Q1.csv"))
    print(total_from_file("sales_2025_Q1.csv"))  # slow again

    print("\n--- Mutable Sale Demo ---")
    sale = Sale(100, "EUR")
    sale = convert_sale(sale, StaticRateFetcher())
    print(sale.amount, sale.currency, sale.converted)

    print("\n--- Manual deltas ---")
    numbers = [120, 150, 200, 180]
    print(compute_sales_deltas(numbers))

    print("\n--- Manual chunk loop ---")
    with open("example.bin", "wb") as f:
        f.write(b"x" * 10_000)
    print(read_large_file("example.bin"))

    print("\n--- Manual JSON loading ---")
    print(load_all_json("rates"))


if __name__ == "__main__":
    main()
