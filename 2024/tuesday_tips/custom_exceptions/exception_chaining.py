def convert_to_integer(text: str) -> int:
    try:
        return int(text)
    except ValueError as e:
        raise TypeError("Conversion to integer failed") from e


def main() -> None:
    try:
        print(convert_to_integer("abc"))
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Cause of the error: {e.__cause__}")


if __name__ == "__main__":
    main()
