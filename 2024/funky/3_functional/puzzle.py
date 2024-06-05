from functools import reduce
from typing import Any, Callable

from chat import ChatFn
from json_helper import parse_json
from prompts import (
    CLUES_PROMPT,
    SOLUTION_PROMPT,
    TITLE_PROMPT,
    WORDS_PROMPT,
)
from pydantic import BaseModel


class PuzzleGame(BaseModel):
    topic: str
    title: str = ""
    solution: str = ""
    words: list[str] = []
    clues: list[str] = []


def filter_words(all_words: list[str], solution: str) -> list[str]:
    words: list[str] = []
    for character in solution:
        for word in all_words:
            if character.lower() in word.lower() and word not in words:
                words.append(word)
                break

    # check that words is the same length as the solution
    assert len(words) == len(solution)

    return words


type Composable = Callable[[Any], Any]


def compose(*functions: Composable) -> Composable:
    def apply(value: Any, fn: Composable) -> Any:
        return fn(value)

    return lambda data: reduce(apply, functions, data)


def generate_puzzle(topic: str, chat: ChatFn, debug: bool = False) -> PuzzleGame:
    puzzle = PuzzleGame(topic=topic)

    puzzle.title = compose(TITLE_PROMPT.substitute, chat)(dict(puzzle))
    puzzle.solution = compose(SOLUTION_PROMPT.substitute, chat)(dict(puzzle))
    if debug:
        print(f"Solution: {puzzle.solution}")

    all_words = compose(WORDS_PROMPT.substitute, chat, parse_json)(dict(puzzle))
    puzzle.words = filter_words(all_words, puzzle.solution)
    if debug:
        print(f"Words: {puzzle.words}")

    puzzle.clues = compose(CLUES_PROMPT.substitute, chat, parse_json)(dict(puzzle))
    return puzzle


def print_puzzle(puzzle: PuzzleGame) -> None:
    # print the title
    print()
    print(puzzle.title)
    print("=" * len(puzzle.title))
    print()

    # compute the maximum index (needed to align the words)
    indices = [
        word.lower().index(puzzle.solution[i].lower())
        for i, word in enumerate(puzzle.words)
    ]
    max_index = max(indices)

    # print the words as blanks, and align them according to the indices in the solution
    # so that the solution forms a column. Each solution character should be printed as 'X' and the rest as '_'
    # align them so that solution forms a vertical column
    for i, word in enumerate(puzzle.words):
        mystery_word = "".join(
            "X " if j == indices[i] else "_ " for j, _ in enumerate(word)
        )
        index_diff = max_index - indices[i]
        blanks = " " * index_diff * 2
        # now add the number of the word and make sure that it also works for double digits
        print(f"{i + 1:02}. {blanks}{mystery_word}")

    # empty line
    print()

    # print the clues and number them
    print("Clues:")
    for i, clue in enumerate(puzzle.clues):
        print(f"{i + 1:02}. {clue}")
