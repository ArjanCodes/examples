def timer():
    pass


def main() -> None:
    timer.counter = 0
    timer.counter += 1
    print(timer.counter)  # Output: 1


if __name__ == "__main__":
    main()
