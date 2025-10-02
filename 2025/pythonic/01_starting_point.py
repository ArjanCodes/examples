from datetime import datetime
import os    

class FitnessTracker:
    def __init__(self):
        self.food_log = []
        self.activity_log = []

    def log_food(self, item, calories, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        f = open("food.csv", "a")
        f.write(f"{date},{item},{calories}\n")
        f.close()
        print(f"Appended food: {item} ({calories} kcal) on {date}")

    def log_activity(self, activity, calories_burned, date=None):
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
        f = open("activities.csv", "a")
        f.write(f"{date},{activity},{calories_burned}\n")
        f.close()
        print(f"Appended activity: {activity} ({calories_burned} kcal) on {date}")

    def run_day_summary(self, date):
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

tracker = FitnessTracker()
tracker.log_food("Banana", 100)
tracker.log_activity("Running", 300)
tracker.run_day_summary(datetime.now().strftime("%Y-%m-%d"))