class CustomError(Exception):
    def __init__(self, message: str, extra_data: dict[str, str]):
        super().__init__(message)
        self.extra_data = extra_data


def main() -> None:
    try:
        raise CustomError("An error occurred", {"key": "value"})
    except CustomError as e:
        print(e)
        print(e.extra_data)  # Prints: {'key': 'value'}


if __name__ == "__main__":
    main()
