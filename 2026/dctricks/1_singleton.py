from dataclasses import dataclass
from typing import ClassVar, Self


class EnvSingleton:
    _instances: ClassVar[dict[str, Self]] = {}

    def __new__(cls, env: str, *args: object, **kwargs: object) -> Self:
        if env not in cls._instances:
            cls._instances[env] = super().__new__(cls)
        return cls._instances[env]


@dataclass
class Config(EnvSingleton):
    env: str
    debug: bool


def main() -> None:
    a = Config("prod", False)
    b = Config("prod", True)
    c = Config("dev", True)

    print(a is b)
    print(a.debug)
    print(a is c)
    print(c.debug)


if __name__ == "__main__":
    main()
