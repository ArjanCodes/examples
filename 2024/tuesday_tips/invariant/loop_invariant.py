def find_max(list_of_integers: list[int]) -> int:
    max_element = list_of_integers[0]  # Assume the first element is the max initially
    for i in range(1, len(list_of_integers)):
        if list_of_integers[i] > max_element:
            max_element = list_of_integers[i]
        # Loop Invariant: At this point in the loop, max_element is the largest item in list_of_integers[0:i].
    return max_element


def main() -> None:
    print(find_max([1, 5, 3, 2, 4]))  # 5
    print(find_max([1, 5, 3, 2, 4, 5, 5, 5, 5, 5]))  # 5


if __name__ == "__main__":
    main()
