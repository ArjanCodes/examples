from dataclasses import dataclass
from datetime import datetime
from typing import Iterator
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

FOOD_CSV = Path("food.csv")
ACTIVITY_CSV = Path("activities.csv")


@dataclass
class Entry:
    date: str
    description: str
    calories: int

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def append_entry(path: Path, entry: Entry) -> None:
    with path.open("a") as f:
        f.write(f"{entry.date},{entry.description},{entry.calories}\n")
    logging.info(f"Appended entry to {path}: {entry.description} ({entry.calories} kcal)")

def log_food(description: str, calories: int, date: str | None = None) -> None:
    if date is None:
        date = today()
    append_entry(FOOD_CSV, Entry(date, description, calories))

def log_activity(description: str, calories: int, date: str | None = None) -> None:
    if date is None:
        date = today()
    append_entry(ACTIVITY_CSV, Entry(date, description, calories))

def read_entries(path: Path) -> Iterator[Entry]:
    try:
        with path.open() as f:
            for line in f:
                date, desc, cals = line.strip().split(",")
                yield Entry(date, desc, int(cals))
    except FileNotFoundError:
        logging.warning(f"File not found: {path}")
        return iter([])


def run_day_summary(date: str) -> None:
    food = list(read_entries(FOOD_CSV))
    activity = list(read_entries(ACTIVITY_CSV))

    food_total = sum(entry.calories for entry in food if entry.date == date)
    activity_total = sum(entry.calories for entry in activity if entry.date == date)
    net = food_total - activity_total

    print(f"\nSummary for {date}")
    print(f"  🍎 Food:     {food_total} kcal")
    print(f"  🏃 Activity: {activity_total} kcal")
    print(f"  ⚖️  Net:       {net} kcal")

    logging.info(f"Daily summary: +{food_total} kcal intake, -{activity_total} burned, net = {net}")

def main() -> None:
    log_food("Banana", 100)
    log_activity("Running", 300)
    run_day_summary(today())

if __name__ == "__main__":
    main()