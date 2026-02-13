from typing import Any, Callable


class SimpleProperty:
    def __init__(self, fget: Callable[[Any], Any]) -> None:
        self.fget = fget

    def __get__(self, instance: Any | None, owner: type) -> Any:
        if instance is None:
            return self
        return self.fget(instance)


class User:
    def __init__(self, first: str, last: str) -> None:
        self.first = first
        self.last = last

    @SimpleProperty
    def full_name(self) -> str:
        return f"{self.first} {self.last}"


def main() -> None:

    u = User("Arjan", "Egges")

    print(u.full_name)
    print(User.full_name)


if __name__ == "__main__":
    main()
