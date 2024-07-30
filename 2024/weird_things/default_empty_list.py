def append_to_list[T](value: T, my_list: list[T] = []) -> list[T]:
    my_list.append(value)
    return my_list


def main() -> None:
    # First call
    result1 = append_to_list(1)
    print(result1)  # Output: [1]

    # Second call
    result2 = append_to_list(2)
    print(result2)  # Output: [1, 2]


if __name__ == "__main__":
    main()
