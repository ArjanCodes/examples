def main() -> None:
    a = 256
    b = 256
    print(a is b)  # Output: True

    c = 257
    d = 257
    print(c is d)  # Output: False


if __name__ == "__main__":
    main()
