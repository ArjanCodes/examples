def bubble_sort(ilist: list[int]) -> None:
    swapped = True
    iterations = 0

    while swapped:
        swapped = False
        for i in range(len(ilist) - iterations - 1):
            if ilist[i] > ilist[i + 1]:
                ilist[i], ilist[i + 1] = ilist[i + 1], ilist[i]
                swapped = True
        iterations += 1


def main() -> None:
    test_list = [120, 68, -20, 0, 5, 67, 14, 99]
    bubble_sort(test_list)
    print(f"Sorted list: {test_list}")


if __name__ == "__main__":
    main()
