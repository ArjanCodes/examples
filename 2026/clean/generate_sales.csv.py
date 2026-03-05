import csv
import random
from pathlib import Path


def main() -> None:
    random.seed(42)
    path = Path("sales.csv")

    countries = ["NL", "BE", "DE"]
    rows = []

    for i in range(1, 51):
        country = "NL" if random.random() < 0.45 else random.choice(countries)
        revenue = round(max(0.0, random.gauss(50, 20)), 2)
        rows.append(
            {"order_id": f"{i:04d}", "country": country, "revenue": f"{revenue:.2f}"}
        )

    # a couple of "bad" rows to show validation noise
    rows.append({"order_id": "BAD1", "country": "NL", "revenue": ""})
    rows.append({"order_id": "BAD2", "country": "NL", "revenue": "-10.00"})

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["order_id", "country", "revenue"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    main()
