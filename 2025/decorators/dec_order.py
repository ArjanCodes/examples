import functools
from functools import lru_cache
from typing import Any, Callable


def authenticate(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("Authenticating user.")
        return func(*args, **kwargs)

    return wrapper


@lru_cache
@authenticate
def fetch_user(user_id: int) -> dict[str, int | str]:
    print("Fetching user from the database.")
    return {"id": user_id, "name": "Alice"}


def main() -> None:
    user = fetch_user(1)
    print(user)

    # Calling again with the same user_id
    user = fetch_user(1)  # Should authenticate again, but it doesn't!
    print(user)

    user = fetch_user(2)
    print(user)


if __name__ == "__main__":
    main()
