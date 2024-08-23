def check_element_existence[T](data: list[T], to_find: T) -> None:
    for num in data:
        if num == to_find:
            print("Exists!")
            break
    else:
        print("Does not exist")


def main() -> None:
    data = [1, 2, 3, 4, 5]
    check_element_existence(data, 4)
    check_element_existence(data, -1)


if __name__ == "__main__":
    main()
