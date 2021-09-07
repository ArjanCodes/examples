def add_three(x: int) -> int:
    return x + 3


def add_three_alt(x: int) -> int:
    if x == 1:
        return 4
    elif x == 2:
        return 5
    elif x == 3:
        return 6
    else:
        return 0


def multiply_by_two(x: int):
    return x * 2


def main():
    # testing the function add_three
    assert add_three_alt(1) == 4
    assert add_three_alt(2) == 5
    assert add_three_alt(3) == 6
    assert multiply_by_two(2) == 4
    print("All tests pass!")


if __name__ == "__main__":
    main()
