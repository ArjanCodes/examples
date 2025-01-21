class NotFoundError(Exception):
    """Custom exception to indicate that an item was not found."""

    ...


USERS: dict[int, dict[str, str | int]] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


def get_user(
    user_id: int, users: dict[int, dict[str, str | int]]
) -> dict[str, int | str] | None:
    return users.get(user_id)


def get_user_(
    user_id: int, users: dict[int, dict[str, str | int]]
) -> dict[str, int | str]:
    if user_id not in users:
        raise NotFoundError(f"User with ID {user_id} not found.")
    return users[user_id]


def main() -> None:
    user_id = 3  # Nonexistent user

    try:
        user = get_user_(user_id, USERS)
        print(user)
    except NotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
