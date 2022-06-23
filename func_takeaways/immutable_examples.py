import random


def main() -> None:
    test_list = [120, 68, -20, 0, 5, 67, 14, 99]

    # built in immutable sort
    sorted_list = sorted(test_list)
    print(f"Original list: {test_list}")
    print(f"Sorted list: {sorted_list}")

    # built in mutable sort
    test_list.sort()
    print(f"Original list: {test_list}")

    # other example of mutable vs immutable operations
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    shuffled_cards = random.sample(cards, k=len(cards))
    print(f"Shuffled cards: {shuffled_cards}")
    print(f"Original cards: {cards}")

    random.shuffle(cards)  # shuffles the cards (mutable)
    print(f"Cards: {cards}")


if __name__ == "__main__":
    main()
