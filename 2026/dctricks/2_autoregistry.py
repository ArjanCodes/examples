from dataclasses import dataclass
from typing import Any, dataclass_transform

REGISTRY: dict[str, type[Any]] = {}


@dataclass_transform()
def event[T](cls: type[T]) -> type[T]:
    dc_cls = dataclass(cls)
    REGISTRY[cls.__name__] = dc_cls
    return dc_cls


@event
class UserCreated:
    user_id: int


@event
class UserDeleted:
    user_id: int


def main() -> None:
    print(REGISTRY)
    e = UserCreated(123)
    print(e)


if __name__ == "__main__":
    main()
