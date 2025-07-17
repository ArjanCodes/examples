import itertools


def main() -> None:
    items = ["a", "b", "c"]

    # All pairs of items
    pairs = list(itertools.combinations(items, 2))
    print("Pairs:", pairs)

    # Infinite counter
    counter = itertools.count(start=10, step=5)
    print("First three counter values:")
    print(next(counter))
    print(next(counter))
    print(next(counter))

    # Cycle through items
    cycle = itertools.cycle(["on", "off"])
    print("Cycle example:")
    for _ in range(4):
        print(next(cycle))

    # Group consecutive identical items
    data = ["a", "a", "b", "b", "b", "c", "a", "a"]
    print("Grouping consecutive items:")
    for key, group in itertools.groupby(data):
        group_list = list(group)
        print(f"{key}: {group_list}")


if __name__ == "__main__":
    main()
