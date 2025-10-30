import csv
from typing import Generator
from performance_tools import measure_performance


def load_sales(path: str) -> Generator[dict[str, str], None, None]:
    print("Streaming CSV data lazily...")
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


@measure_performance
def analyse_sales(path: str) -> float:
    return sum(float(s["amount"]) for s in load_sales(path))


@measure_performance
def count_sales(path: str) -> int:
    return sum(1 for _ in load_sales(path))


def main() -> None:
    path = "sales.csv"

    while True:
        print("\nChoose an option:")
        print("1. Analyse sales data (streaming)")
        print("2. Count total sales records (streaming)")
        print("3. Quit")

        choice = input("> ")

        if choice == "1":
            total = analyse_sales(path)
            print(f"Total sales: ${total:.2f}")
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