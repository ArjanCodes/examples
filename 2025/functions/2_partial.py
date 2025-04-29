from functools import partial


def power(base: float, exponent: float) -> float:
    return base**exponent


def main() -> None:
    # Create a partial function that always raises to the power of 2
    square = partial(power, exponent=2)
    print(square(4))  # 16


if __name__ == "__main__":
    main()
