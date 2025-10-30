import csv
import time
from typing import Generator
from performance_tools import measure_performance


def load_sales(path: str) -> Generator[dict[str, str], None, None]:
    print("Streaming CSV data lazily...")
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def get_conversion_rates() -> dict[str, float]:
    print("Fetching conversion rates from remote service...")
    time.sleep(2)
    return {"USD": 1.0, "EUR": 1.1, "JPY": 0.007}


@measure_performance
def analyse_sales(path: str, currency: str) -> float:
    total = sum(float(s["amount"]) for s in load_sales(path))
    rate = get_conversion_rates().get(currency, 1.0)
    return total * rate


@measure_performance
def count_sales(path: str) -> int:
    return sum(1 for _ in load_sales(path))


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