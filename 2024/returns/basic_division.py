from returns.result import Failure, Result, Success


def divide(a: int, b: int) -> Result[int, str]:
    return Success(a // b) if b != 0 else Failure("Cannot divide by zero")


def main() -> None:
    result = divide(10, 2).value_or("Error")
    error_result = divide(10, 0).value_or("Error")

    print(result)
    print(error_result)


if __name__ == "__main__":
    main()
