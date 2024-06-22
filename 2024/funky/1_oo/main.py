import os

from chat import chatter
from dotenv import load_dotenv
from puzzle import PuzzleGame


def main() -> None:
    load_dotenv()

    openai_key = os.getenv("OPENAI_KEY")
    if not openai_key:
        raise ValueError(
            "No API key found. Please set your OPENAI_KEY in the .env file."
        )

    chat = chatter(api_key=openai_key)

    print("Generating puzzle...")

    puzzle = PuzzleGame(
        topic="Python data structures",
    )
    puzzle.generate(chat, debug=True)
    puzzle.print()


if __name__ == "__main__":
    main()
