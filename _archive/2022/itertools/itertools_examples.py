import itertools


def main() -> None:
    # Counting
    for i in itertools.count(10):
        print(i)
        if i == 15:
            break

    # Repeating
    for i in itertools.repeat(10, 4):
        print(i)

    # Accumulate
    for i in itertools.accumulate(range(1, 11)):
        print(i)

    # Get all permutations of length 2
    items = ["a", "b", "c"]
    perms = itertools.permutations(items, 2)

    # Print the permutations
    for perm in perms:
        print(perm)

    # Print all permutations as a single list
    print(list(itertools.permutations(items)))

    # Combining different iterables
    for item in itertools.chain(items, range(5)):
        print(item)

    print(list(itertools.permutations(range(3), 2)))

    # Get all combinations of length 2 (order does not matter)
    print(list(itertools.combinations(items, 2)))

    # Get all combinations with replacement of length 2
    print(list(itertools.combinations_with_replacement(items, 2)))

    # Itertools chain
    more_items = ["d", "e", "f"]
    all_items = itertools.chain(items, more_items)
    print(list(all_items))

    # Filter false
    print(list(itertools.filterfalse(lambda x: x % 2 == 0, range(10))))

    # Starmap
    print(list(itertools.starmap(lambda x, y: x * y, [(2, 6), (8, 4), (5, 3)])))

    # Tee
    a, b, c = itertools.tee(range(3), 3)
    print(list(a))
    print(list(b))
    print(list(c))


if __name__ == "__main__":
    main()
