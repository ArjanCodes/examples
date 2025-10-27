from datetime import datetime
import os

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def log_food(item: str, calories: int, date: str | None = None) -> None:
    if date is None:
        date = today()
    with open("food.csv", "a") as f:
        f.write(f"{date},{item},{calories}\n")
    print(f"Appended food: {item} ({calories} kcal) on {date}")

def log_activity(item: str, calories: int, date: str | None = None) -> None:
    if date is None:
        date = today()
    with open("activities.csv", "a") as f:
        f.write(f"{date},{item},{calories}\n")
    print(f"Appended activity: {item} ({calories} kcal) on {date}")


def run_day_summary(date: str) -> None:
    food: list[int] = []
    try:
        with open("food.csv") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == date:
                    food.append(int(parts[2]))
    except FileNotFoundError:
        print("Could not read food.csv")

    activity: list[int] = []
    try:
        with open("activities.csv") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == date:
                    activity.append(int(parts[2]))
    except FileNotFoundError:
        print("Could not read activities.csv")

    food_total = sum(food)
    activity_total = sum(activity)
    net = food_total - activity_total

    print(f"\nSummary for {date}")
    print(f"  🍎 Food:     {food_total} kcal")
    print(f"  🏃 Activity: {activity_total} kcal")
    print(f"  ⚖️  Net:       {net} kcal")

log_food("Banana", 100)
log_activity("Running", 300)
run_day_summary(today())