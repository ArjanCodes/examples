from returns.result import safe


@safe
def divide(a: int, b: int) -> int:
    return a // b


def main() -> None:
    safe_result = divide(10, 2)  # Success(5)
    error_result = divide(10, 0)  # Failure(ZeroDivisionError)

    print(safe_result)
    print(error_result)

    print(divide(10, 2).value_or(-1))  # Outputs: 5
    print(divide(10, 0).value_or(-1))  # Outputs: -1


if __name__ == "__main__":
    main()
