import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration ---
OUTPUT_FILE = Path("sales.csv")
NUM_ROWS = 10_000_000
PRINT_EVERY = 100_000  # progress update

# --- Data generation helpers ---
def random_date(start: datetime, end: datetime) -> str:
    """Return a random date between start and end as YYYY-MM-DD."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def random_amount() -> float:
    """Return a random sales amount."""
    return round(random.uniform(5.0, 500.0), 2)

def random_country() -> str:
    """Return a random country."""
    return random.choice([
        "US", "DE", "NL", "FR", "JP", "IN", "BR", "GB", "CA", "AU"
    ])

# --- Main generator ---
def generate_sales_csv(path: Path, num_rows: int) -> None:
    """Generate a large CSV file with sales data."""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 1, 1)

    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "country", "product", "amount"])

        for i in range(1, num_rows + 1):
            writer.writerow([
                i,
                random_date(start_date, end_date),
                random_country(),
                f"Product-{random.randint(1, 1000)}",
                random_amount(),
            ])
            if i % PRINT_EVERY == 0:
                print(f"Wrote {i:,} rows...")

    print(f"✅ Done! Wrote {num_rows:,} rows to {path.resolve()}")

# --- Run ---
if __name__ == "__main__":
    generate_sales_csv(OUTPUT_FILE, NUM_ROWS)