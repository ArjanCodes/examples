from typing import Callable


ValidatorFn = Callable[[int], bool]


def validate_pipeline(validators: list[ValidatorFn]) -> ValidatorFn:
    def validator(value: int) -> bool:
        return all(validator(value) for validator in validators)

    return validator


# Define validator functions
def is_even(value: int) -> bool:
    return value % 2 == 0


def is_positive(value: int) -> bool:
    return value > 0


def main() -> None:
    validator = validate_pipeline([is_even, is_positive])

    # Perform validation
    result = validator(4)
    print(result)  # Output: True

    result = validator(7)
    print(result)  # Output: False


if __name__ == "__main__":
    main()
