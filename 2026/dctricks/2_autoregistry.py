from dataclasses import dataclass
from typing import Self


class Event:
    registry: dict[str, type[Self]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        Event.registry[cls.__name__] = cls


@dataclass
class UserCreated(Event):
    user_id: int


@dataclass
class UserDeleted(Event):
    user_id: int


def main() -> None:
    print(Event.registry)


if __name__ == "__main__":
    main()
