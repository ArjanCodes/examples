from typing import Iterable, Sized


def count(words: Iterable[Sized]) -> list[int]:
    result = []
    for word in words:
        result.append(len(word))
    return result


def main() -> None:
    words = ["apple", "banana", "cherry"]
    result = count(words)
    print(result)


if __name__ == "__main__":
    main()
