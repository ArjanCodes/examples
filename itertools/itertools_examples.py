from itertools import (
    accumulate,
    chain,
    combinations,
    combinations_with_replacement,
    count,
    filterfalse,
    permutations,
    repeat,
    starmap,
    tee,
)


def main() -> None:
    # Counting
    for i in count(10):
        print(i)
        if i == 15:
            break

    # Repeating
    for i in repeat(10, 4):
        print(i)

    # Accumulate
    for i in accumulate(range(1, 11)):
        print(i)

    # Get all permutations of length 2
    items = ["a", "b", "c"]
    perms = permutations(items, 2)

    # Print the permutations
    for perm in perms:
        print(perm)

    # Print all permutations as a single list
    print(list(permutations(items)))

    # Combining different iterables
    for item in chain(items, range(5)):
        print(item)

    print(list(permutations(range(3), 2)))

    # Get all combinations of length 2 (order does not matter)
    print(list(combinations(items, 2)))

    # Get all combinations with replacement of length 2
    print(list(combinations_with_replacement(items, 2)))

    # Itertools chain
    more_items = ["d", "e", "f"]
    all_items = chain(items, more_items)
    print(list(all_items))

    # Filter false
    print(list(filterfalse(lambda x: x % 2 == 0, range(10))))

    # Starmap
    print(list(starmap(lambda x, y: x * y, [(2, 6), (8, 4), (5, 3)])))

    # Tee
    a, b, c = tee(range(3), 3)
    print(list(a))
    print(list(b))
    print(list(c))


if __name__ == "__main__":
    main()
