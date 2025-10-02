from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

@dataclass
class Entry:
    date: str
    description: str
    calories: int

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def append_entry(filename: str, entry: Entry) -> None:
    with open(filename, "a") as f:
        f.write(f"{entry.date},{entry.description},{entry.calories}\n")
    print(f"Appended to {filename}: {entry.description} ({entry.calories} kcal)")


def read_entries(filename: str) -> Iterator[Entry]:
    try:
        with open(filename) as f:
            for line in f:
                date, desc, cals = line.strip().split(",")
                yield Entry(date, desc, int(cals))
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return iter([])

def run_day_summary(date: str) -> None:
    food = list(read_entries("food.csv"))
    activity = list(read_entries("activities.csv"))

    food_total = sum(entry.calories for entry in food if entry.date == date)
    activity_total = sum(entry.calories for entry in activity if entry.date == date)
    net = food_total - activity_total

    print(f"\nSummary for {date}")
    print(f"  🍎 Food:     {food_total} kcal")
    print(f"  🏃 Activity: {activity_total} kcal")
    print(f"  ⚖️  Net:       {net} kcal")



append_entry("food.csv", Entry(today(), "Banana", 100))
append_entry("activities.csv", Entry(today(), "Running", 300))
run_day_summary(today())