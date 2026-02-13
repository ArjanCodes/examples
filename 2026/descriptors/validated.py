from typing import Any, Callable, Self

Validator = Callable[[str, Any], None]


def non_empty(field: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")


def min_value(n: int) -> Validator:
    def _v(field: str, value: Any) -> None:
        if value < n:
            raise ValueError(f"{field} must be >= {n}")

    return _v


class ValidatedField[T]:
    def __init__(
        self,
        cast: Callable[[Any], T],
        validators: tuple[Validator, ...] = (),
    ) -> None:
        self.cast = cast
        self.validators = validators
        self.name: str = ""
        self.storage_name: str = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type) -> T | Self | None:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance: object, value: Any) -> None:
        casted = self.cast(value)
        for v in self.validators:
            v(self.name, casted)
        setattr(instance, self.storage_name, casted)


class Customer:
    name: ValidatedField[str] = ValidatedField(cast=str, validators=(non_empty,))
    age: ValidatedField[int] = ValidatedField(cast=int, validators=(min_value(18),))

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


def main() -> None:

    c = Customer("Arjan", 48)
    print(c.name, c.age)

    try:
        c.name = "   "
    except ValueError as e:
        print(e)

    try:
        c.age = 17
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
