def parse_numbers(user_inputs: list[str]) -> list[int]:
    valid_numbers: list[int] = []
    for value in user_inputs:
        try:
            number = int(value)
            valid_numbers.append(number)
        except ValueError:
            print(f"Invalid input skipped: {value}")
    return valid_numbers


def main() -> None:
    user_inputs: list[str] = ["10", "20", "invalid", "30"]
    valid_numbers = parse_numbers(user_inputs)
    print("Valid numbers:", valid_numbers)


if __name__ == "__main__":
    main()
