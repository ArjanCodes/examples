import random
from pathlib import Path


def generate_csv(path: Path, rows: int = 10_000_000) -> None:
    """
    Generate a CSV file with `rows` number of sales entries.
    Format: sale_id,amount
    Example: 1,12.50
    """
    with path.open("w") as f:
        for i in range(1, rows + 1):
            amount = round(random.uniform(1.0, 500.0), 2)
            f.write(f"{i},{amount}\n")

    print(f"Generated {rows} rows → {path}")


def main() -> None:
    path = Path("sales_2025_Q1.csv")
    generate_csv(path)


if __name__ == "__main__":
    main()
