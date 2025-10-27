def main() -> None:
    words = ["code", "python", "ai", "refactor", "bug"]

    length_map: dict[str, int] = {}
    for word in words:
        if len(word) > 4:
            length_map[word] = len(word)

    print(length_map)

    # now with a dict comprehension
    length_map_comp = {word: len(word) for word in words if len(word) > 4}
    print(length_map_comp)

if __name__ == "__main__":
    main()