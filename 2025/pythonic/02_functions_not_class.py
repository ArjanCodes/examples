from datetime import datetime
import os

def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def log_food(item, calories, date=None):
    if date is None:
        date = today()
    f = open("food.csv", "a")
    f.write(f"{date},{item},{calories}\n")
    f.close()
    print(f"Appended food: {item} ({calories} kcal) on {date}")

def log_activity(item, calories, date=None):
    if date is None:
        date = today()
    f = open("activities.csv", "a")
    f.write(f"{date},{item},{calories}\n")
    f.close()
    print(f"Appended activity: {item} ({calories} kcal) on {date}")

def run_day_summary(date):
    food = []
    if os.path.exists("food.csv"):
        f = open("food.csv")
        for line in f:
            parts = line.strip().split(",")
            if parts[0] == date:
                food.append(int(parts[2]))
        f.close()
    else:
        print("Could not read food.csv")

    activity = []
    if os.path.exists("activities.csv"):
        f = open("activities.csv")
        for line in f:
            parts = line.strip().split(",")
            if parts[0] == date:
                activity.append(int(parts[2]))
        f.close()
    else:
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