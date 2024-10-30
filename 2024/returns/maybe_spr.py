from dataclasses import dataclass

from returns.maybe import Maybe, Nothing, Some


@dataclass
class User:
    id: int
    name: str


USERS = {1: User(1, "Alice"), 2: User(2, "Bob")}


# Using a Maybe container to handle optional values
def find_user(user_id) -> Maybe[User]:
    return Some(USERS[user_id]) if user_id in USERS else Nothing


def handle_user_data(user_id):
    match find_user(user_id):
        case Some(user):
            print(f"User found: {user.name}")
        case Nothing:
            print("No user found")


def main() -> None:
    handle_user_data(1)  # Outputs: User found: Alice
    handle_user_data(3)  # Outputs: No user found


if __name__ == "__main__":
    main()
