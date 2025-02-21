from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool


USERS: dict[int, User] = {
    1: User(id=1, name="Alice", email="alice@example.com", active=False),
    2: User(id=2, name="Bob", email="bob@example.com", active=True),
}


def get_first_active_user() -> User | None:
    for user in USERS.values():
        if user.active:
            return user
    return None


def get_user(user_id: int) -> User | None:
    return USERS.get(user_id)


def main() -> None:
    # Existing user
    user = get_user(1)
    print(user)

    # Non-existing user
    user = get_user(3)
    print(user)

    # First active user
    user = get_first_active_user()
    print(user)


if __name__ == "__main__":
    main()
