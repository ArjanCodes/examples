def parse_numbers(user_inputs: list[str]) -> list[int]:
    def safe_convert(value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            print(f"Invalid input skipped: {value}")
            return None

    return list(filter(lambda x: x is not None, map(safe_convert, user_inputs)))


def main() -> None:
    user_inputs: list[str] = ["10", "20", "invalid", "30"]
    valid_numbers = parse_numbers(user_inputs)
    print("Valid numbers:", valid_numbers)


if __name__ == "__main__":
    main()
