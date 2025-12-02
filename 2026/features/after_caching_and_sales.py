import json
from contextlib import suppress
from dataclasses import dataclass, replace
from functools import cache
from itertools import pairwise
from pathlib import Path
from typing import Any, Protocol, Sequence


@cache
def total_from_file(path: Path) -> float:
    """Compute total sales by reading and parsing a large CSV file."""
    print(f"Reading file: {path.name}")
    total = 0.0
    with path.open() as f:
        for line in f:
            _, amount = line.strip().split(",")
            total += float(amount)
    return total


class RateFetcher(Protocol):
    def get_rate(self, currency: str) -> float: ...


class StaticRateFetcher:
    """Simple fake fetcher for demonstration."""

    def get_rate(self, currency: str) -> float:
        rates = {"EUR": 1.1, "USD": 1.0}
        return rates.get(currency, 1.0)


@dataclass(frozen=True)
class Sale:
    amount: float
    currency: str
    converted: float | None = None


def convert_sale(sale: Sale, fetcher: RateFetcher) -> Sale:
    rate = fetcher.get_rate(sale.currency)
    return replace(sale, converted=sale.amount * rate)


def compute_sales_deltas(numbers: Sequence[float]) -> list[float]:
    return [b - a for a, b in pairwise(numbers)]


def read_large_file(path: Path) -> int:
    """Count bytes using streaming reads."""
    total = 0
    with path.open("rb") as f:
        while chunk := f.read(4096):
            total += len(chunk)
    return total


def load_all_json(directory: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for path in directory.glob("*.json"):
        with suppress(Exception):
            results[path.stem] = json.loads(path.read_text())
    return results


def main() -> None:
    print("\n--- Caching Demo (File Parsing) ---")
    print(total_from_file(Path("sales_2025_Q1.csv")))  # reads the file
    print(total_from_file(Path("sales_2025_Q1.csv")))  # instant

    print("\n--- Immutable Dataclass Demo ---")
    sale = Sale(amount=100, currency="EUR")
    new_sale = convert_sale(sale, StaticRateFetcher())
    print(new_sale)

    print("\n--- Pairwise Demo ---")
    numbers = [120, 150, 200, 180]
    print(compute_sales_deltas(numbers))

    print("\n--- Assignment Expression Demo ---")
    binary = Path("example.bin")
    binary.write_bytes(b"x" * 10_000)
    print(read_large_file(binary))

    print("\n--- Pathlib + suppress Demo ---")
    directory = Path("rates")
    directory.mkdir(exist_ok=True)
    (directory / "eur.json").write_text(json.dumps({"rate": 1.1}))
    (directory / "broken.json").write_text("NOT JSON")
    print(load_all_json(directory))

    print("\nDone!")


if __name__ == "__main__":
    main()
