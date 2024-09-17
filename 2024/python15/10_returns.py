from returns.result import Failure, Success


def divide(a: int, b: int):
    if b == 0:
        return Failure("Division by zero!")
    return Success(a / b)


def main():
    result = divide(10, 0)

    match result:
        case Success(value):
            print(f"Result: {value}")
        case Failure(error):
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
