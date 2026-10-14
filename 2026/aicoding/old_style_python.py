from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Repository(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get(self, index: int) -> Optional[T]:
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def get_all(self) -> List[T]:
        return self.items.copy()


@dataclass
class User:
    name: str
    email: str


def main() -> None:
    users = Repository[User]()

    users.add(User("Alice", "alice@example.com"))
    users.add(User("Bob", "bob@example.com"))

    print(users.get(0))
    print(users.get_all())


if __name__ == "__main__":
    main()
