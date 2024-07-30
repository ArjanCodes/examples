def main() -> None:
    a = [1, 2, 3]
    b = a  # b is now a reference to a
    a += [4]
    print(b)  # Output: [1, 2, 3, 4]

    s = "hello"
    t = s  # t is now a reference to s
    s += " world"
    print(t)  # Output: "hello"


if __name__ == "__main__":
    main()
