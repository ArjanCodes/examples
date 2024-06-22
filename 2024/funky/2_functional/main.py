import os

from chat import chatter
from dotenv import load_dotenv
from puzzle import generate_puzzle, print_puzzle


def main() -> None:
    load_dotenv()

    openai_key = os.getenv("OPENAI_KEY")
    if not openai_key:
        raise ValueError(
            "No API key found. Please set your OPENAI_KEY in the .env file."
        )

    chat = chatter(api_key=openai_key)

    print("Generating puzzle...")

    puzzle = generate_puzzle("Python data structures", chat, debug=True)
    print_puzzle(puzzle)


if __name__ == "__main__":
    main()
