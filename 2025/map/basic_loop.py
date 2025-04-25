from typing import TypedDict


class User(TypedDict):
    name: str
    age: int


def main() -> None:
    users: list[User] = [
        {"name": "Alice", "age": 28},
        {"name": "Bob", "age": 17},
        {"name": "Carol", "age": 35},
    ]

    adult_names: list[str] = []

    for user in users:
        if user["age"] >= 18:
            adult_names.append(user["name"].upper())

    print(adult_names)


if __name__ == "__main__":
    main()
