from dataclasses import dataclass
from typing import Any, Callable, Final, Iterator, Tuple

VALIDATOR_ATTR: Final[str] = "_validate_field"


def validator(field_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        setattr(func, VALIDATOR_ATTR, field_name)
        return func

    return decorator


class Validatable:
    """
    Base class for dataclasses that want field-level validation/transforms.

    Contract:
    - Validators are instance methods decorated with @validator("<fieldname>").
    - Validator methods take the current field value and return the new value.
    """

    def __post_init__(self) -> None:
        for field_name, validate in self._validators():
            if not hasattr(self, field_name):
                raise AttributeError(
                    f"{self.__class__.__name__} has validator for unknown field '{field_name}'"
                )

            value = getattr(self, field_name)
            new_value = validate(value)
            setattr(self, field_name, new_value)

    def _validators(self) -> Iterator[Tuple[str, Callable[[Any], Any]]]:
        """
        Yield (field_name, validator_method) for every validator defined on this instance.
        """
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if not callable(method):
                continue

            field_name = getattr(method, VALIDATOR_ATTR, None)
            if field_name is None:
                continue

            # At this point it's a validator. We expect it to be a bound instance method:
            # Callable[[Any], Any]
            yield field_name, method  # type: ignore[misc]


@dataclass
class User(Validatable):
    name: str
    age: int

    @validator("age")
    def validate_age(self, value: int) -> int:
        if value < 0:
            raise ValueError("Age cannot be negative")
        return value

    @validator("name")
    def validate_name(self, value: str) -> str:
        return value.strip().title()


def main() -> None:
    print(User("   alice   ", 30))
    try:
        print(User("bob", -5))
    except ValueError as e:
        print(f"Caught error as expected: {e}")


if __name__ == "__main__":
    main()
