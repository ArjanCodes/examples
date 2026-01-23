from dataclasses import dataclass
from typing import ClassVar, Self


@dataclass(frozen=True, slots=True)
class Config:
    env: str
    debug: bool = False

    _cache: ClassVar[dict[str, Self]] = {}

    @classmethod
    def for_env(cls, env: str, debug: bool = False) -> Self:
        # First call wins for a given env
        if env not in cls._cache:
            cls._cache[env] = cls(env=env, debug=debug)
        return cls._cache[env]


def main() -> None:
    a = Config.for_env("prod", debug=True)
    b = Config.for_env("prod")  # does not reset debug
    c = Config.for_env("dev", debug=True)

    print(a is b)  # True
    print(a.debug)  # True
    print(b.debug)  # True
    print(a is c)  # False
    print(c.debug)  # True


if __name__ == "__main__":
    main()
