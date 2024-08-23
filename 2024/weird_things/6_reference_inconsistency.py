def f():
    return 1


def main() -> None:
    print(f())  # Output: 1
    a = [1, 2, 3]
    b = a  # b is now a reference to a
    print(id(a))
    print(id(b))
    a += [4]
    print(b)  # Output: [1, 2, 3, 4]

    s = "hello"
    t = s  # t is now a reference to s
    print(id(s))
    print(id(t))
    s += " world"
    print(t)  # Output: "hello"


if __name__ == "__main__":
    main()
