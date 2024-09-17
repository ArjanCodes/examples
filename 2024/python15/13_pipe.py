from pipe import select, where


def main():
    numbers = range(10)
    result = list(numbers | where(lambda x: x % 2 == 0) | select(lambda x: x * 2))
    print(result)  # Output: [0, 4, 8, 12, 16]


if __name__ == "__main__":
    main()
