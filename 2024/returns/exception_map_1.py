from returns.result import Failure, Result, Success


def divide(a: int, b: int) -> Result[int, str]:
    try:
        return Success(a // b)
    except ZeroDivisionError:
        return Failure("Division by zero")


def main() -> None:
    safe_result = divide(10, 2)  # Success(5)
    error_result = divide(10, 0)  # Failure("Division by zero")

    print(safe_result)
    print(error_result)

    print(divide(10, 2).value_or(-1))  # Outputs: 5
    print(divide(10, 0).value_or(-1))  # Outputs: -1


if __name__ == "__main__":
    main()
