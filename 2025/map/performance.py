import time
from typing import TypedDict


# Setup
class User(TypedDict):
    name: str
    age: int


def main() -> None:
    users: list[User] = [
        {"name": "User" + str(i), "age": i % 50}
        for i in range(10_000_000)  # Increased size
    ]

    # For loop
    start: float = time.perf_counter()
    adult_names: list[str] = []
    for user in users:
        if user["age"] >= 18:
            adult_names.append(user["name"].upper())
    end: float = time.perf_counter()
    print("For loop:", end - start)

    # Map/filter
    start = time.perf_counter()
    adult_users = filter(lambda u: u["age"] >= 18, users)
    adult_names = list(map(lambda u: u["name"].upper(), adult_users))
    end = time.perf_counter()
    print("Map/filter:", end - start)

    # List comprehension
    start = time.perf_counter()
    adult_names = [user["name"].upper() for user in users if user["age"] >= 18]
    end = time.perf_counter()
    print("List comp:", end - start)


if __name__ == "__main__":
    main()
