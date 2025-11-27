import csv
from performance_tools import measure_performance


def load_sales(path: str) -> list[dict[str, str]]:
    """Eagerly load the entire CSV into memory."""
    print("Loading CSV data...")
    with open(path) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


@measure_performance
def analyse_sales(sales: list[dict[str, str]]) -> float:
    total = 0.0
    for i, sale in enumerate(sales, start=1):
        total += float(sale["amount"])
    return total


@measure_performance
def count_sales(sales: list[dict[str, str]]) -> int:
    return len(sales)


def main() -> None:
    sales = load_sales("sales.csv")  # ❌ slow startup

    while True:
        print("\nChoose an option:")
        print("1. Analyse sales data")
        print("2. Count total sales records")
        print("3. Quit")

        choice = input("> ")

        if choice == "1":
            total = analyse_sales(sales)
            print(f"Total sales: ${total:.2f}")
        elif choice == "2":
            count = count_sales(sales)
            print(f"Number of sales: {count:,}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()