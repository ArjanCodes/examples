from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator

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
    print(f"Appended to {path}: {entry.description} ({entry.calories} kcal)")

def read_entries(path: Path) -> Iterator[Entry]:
    try:
        with path.open() as f:
            for line in f:
                date, desc, cals = line.strip().split(",")
                yield Entry(date, desc, int(cals))
    except FileNotFoundError:
        print(f"File not found: {path}")
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

append_entry(FOOD_CSV, Entry(today(), "Banana", 100))
append_entry(ACTIVITY_CSV, Entry(today(), "Running", 300))
run_day_summary(today())