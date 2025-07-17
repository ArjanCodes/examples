from functools import cache, partial


@cache
def power(base: int, exponent: int) -> int:
    print(f"Computing {base}^{exponent}")
    return base**exponent


def main() -> None:
    # cached power function
    print("Calculating powers with caching:")
    print("Power of 2^10:", power(2, 10))
    print("Power of 3^5:", power(3, 5))
    print("Power of 2^10 again (cached):", power(2, 10))

    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    print("Square of 5:", square(5))
    print("Cube of 2:", cube(2))
    print("Square of 5 again (cached):", square(5))


if __name__ == "__main__":
    main()
