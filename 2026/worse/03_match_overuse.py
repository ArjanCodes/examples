from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    name: str
    is_admin: bool


def can_delete_with_match(user: User) -> bool:
    # Pattern matching adds ceremony to a simple predicate.
    match user:
        case User(is_admin=True):
            return True
        case User(is_admin=False):
            return False
        case _:
            raise AssertionError("Unexpected user state")


def can_delete(user: User) -> bool:
    return user.is_admin


def main() -> None:
    user = User(name="Ada", is_admin=True)
    print(can_delete_with_match(user))
    print(can_delete(user))


if __name__ == "__main__":
    main()
