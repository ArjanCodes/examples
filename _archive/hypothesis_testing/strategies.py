from hypothesis.strategies import integers


def main() -> None:
    # a few strategy examples

    # basic integers
    print(integers().example())

    # within a range
    print(integers(min_value=0, max_value=10).example())

    # filtered integers
    print(integers(min_value=0, max_value=10).filter(lambda x: x % 2 == 1).example())


if __name__ == "__main__":
    main()
