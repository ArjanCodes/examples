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

    adult_users = filter(lambda u: u["age"] >= 18, users)
    adult_names = list(map(lambda u: u["name"].upper(), adult_users))

    print(adult_names)


if __name__ == "__main__":
    main()
