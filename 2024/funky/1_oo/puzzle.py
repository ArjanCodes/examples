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

    def generate(self, chat: ChatFn, debug: bool = False):
        self.title = self._generate_title(chat)
        self.solution = self._generate_solution(chat)
        if debug:
            print(f"Solution: {self.solution}")
        all_words = self._generate_words(chat)
        self.words = self._filter_words(all_words)
        if debug:
            print(f"Words: {self.words}")
        self.clues = self._generate_clues(chat)

    def _generate_title(self, chat: ChatFn) -> str:
        return chat(TITLE_PROMPT.substitute(topic=self.topic))

    def _generate_solution(self, chat: ChatFn) -> str:
        return chat(SOLUTION_PROMPT.substitute(topic=self.topic))

    def _generate_words(self, chat: ChatFn) -> list[str]:
        response = chat(
            WORDS_PROMPT.substitute(solution=self.solution, topic=self.topic)
        )
        return parse_json(response)

    def _filter_words(self, all_words: list[str]) -> list[str]:
        words: list[str] = []
        for character in self.solution:
            for word in all_words:
                if character.lower() in word.lower() and word not in words:
                    words.append(word)
                    break

        # check that words is the same length as the solution
        assert len(words) == len(self.solution)

        return words

    def _generate_clues(self, chat: ChatFn) -> list[str]:
        response = chat(CLUES_PROMPT.substitute(words=self.words))
        return parse_json(response)

    def print(self) -> None:
        # print the title
        print()
        print(self.title)
        print("=" * len(self.title))
        print()

        # compute the maximum index (needed to align the words)
        indices = [
            word.lower().index(char.lower())
            for char, word in zip(self.solution, self.words)
        ]
        max_index = max(indices)

        # print the words as blanks, and align them according to the indices in the solution
        # so that the solution forms a column. Each solution character should be printed as 'X' and the rest as '_'
        # align them so that solution forms a vertical column
        for i, word in enumerate(self.words):
            mystery_word = "".join(
                "X " if j == indices[i] else "_ " for j, _ in enumerate(word)
            )

            index_diff = max_index - indices[i]
            blanks = "  " * index_diff
            # now add the number of the word and make sure that it also works for double digits
            print(f"{i + 1:02}. {blanks}{mystery_word}")

        # empty line
        print()

        # print the clues and number them
        print("Clues:")
        for i, clue in enumerate(self.clues):
            print(f"{i + 1:02}. {clue}")
