import heapq

def main() -> None:
    # Initial tasks with priorities
    tasks = [
        (3, "Send email to client"),
        (2, "Write documentation"),
        (1, "Fix critical bug"),
    ]

    heapq.heapify(tasks)

    print("Starting task processing...")

    while tasks:
        priority, task = heapq.heappop(tasks)
        print(f"Processing task: {task} (priority {priority})")

        # Dynamically add new tasks
        if task == "Fix critical bug":
            print("New urgent task arrived!")
            heapq.heappush(tasks, (0, "Deploy hotfix"))

        if task == "Write documentation":
            heapq.heappush(tasks, (4, "Refactor old module"))

if __name__ == "__main__":
    main()