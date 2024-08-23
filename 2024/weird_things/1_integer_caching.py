def main() -> None:
    a = int("256")
    b = int("256")
    print(a is b)  # Output: True

    c = int("257")
    d = int("257")
    print(c is d)  # Output: False


if __name__ == "__main__":
    main()
