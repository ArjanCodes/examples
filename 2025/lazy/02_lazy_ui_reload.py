import csv
from performance_tools import measure_performance


def load_sales(path: str) -> list[dict[str, str]]:
    print("Loading CSV data lazily...")
    with open(path) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


@measure_performance
def analyse_sales(path: str) -> float:
    sales = load_sales(path)
    return sum(float(s["amount"]) for s in sales)


@measure_performance
def count_sales(path: str) -> int:
    sales = load_sales(path)
    return len(sales)


def main() -> None:
    path = "sales.csv"

    while True:
        print("\nChoose an option:")
        print("1. Analyse sales data")
        print("2. Count total sales records")
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