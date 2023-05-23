from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Validator:
    validators: list[Callable[[int], bool]] = field(default_factory=list)

    def add_validator(self, validator: Callable[[int], bool]) -> None:
        self.validators.append(validator)

    def __call__(self, value: int) -> bool:
        return all(validator(value) for validator in self.validators)


# Define validator functions
def is_even(value: int) -> bool:
    return value % 2 == 0


def is_positive(value: int) -> bool:
    return value > 0


def main() -> None:
    # Create a Validator instance with multiple validators
    validator = Validator(validators=[is_even, is_positive])

    # Perform validation
    result = validator(4)
    print(result)  # Output: True

    result = validator(7)
    print(result)  # Output: False


if __name__ == "__main__":
    main()
