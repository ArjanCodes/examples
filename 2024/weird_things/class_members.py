class X:
    some_attribute = 1


def main() -> None:
    a = X()
    b = X()
    print(a.some_attribute)
    print(b.some_attribute)
    X.some_attribute = 2
    print(a.some_attribute)
    print(b.some_attribute)
    a.some_attribute = 3
    print(a.some_attribute)
    print(b.some_attribute)
    print(X.some_attribute)  # what will this print?


if __name__ == "__main__":
    main()
