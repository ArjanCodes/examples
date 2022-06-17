def merge(left: list[int], right: list[int]) -> list[int]:
    if not left:
        return right
    elif not right:
        return left
    elif left[0] < right[0]:
        return [left[0]] + merge(left[1:], right)
    else:
        return [right[0]] + merge(left, right[1:])


def merge_sort(ilist: list[int]) -> list[int]:
    if len(ilist) < 2:
        return ilist
    left = merge_sort(ilist[: len(ilist) // 2])
    right = merge_sort(ilist[len(ilist) // 2 :])
    return merge(left, right)


def main() -> None:
    test_list = [120, 68, -20, 0, 5, 67, 14, 99]
    sorted_list = merge_sort(test_list)
    print(f"Original list: {test_list}")
    print(f"Sorted list: {sorted_list}")


if __name__ == "__main__":
    main()
