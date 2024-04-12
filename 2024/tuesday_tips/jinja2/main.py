import os

from dotenv import load_dotenv

from ainode import chat, compose, debug, embed, jinja_template, merge, parse_json

load_dotenv()


def main() -> None:
    api_key = os.getenv("OPENAI_KEY")
    if not api_key:
        raise ValueError(
            "No API key found. Please set your OPENAI_KEY in the .env file."
        )
    chat_fn = chat(api_key)

    quiz = {
        "question_count": 5,
        "quiz_difficulty": "easy",
        "quiz_type": "mix",
        "text": "Software design principles.",
    }

    chain_fn = compose(
        jinja_template("prompts/create_quiz.jinja"),
        chat_fn,
        debug,
        parse_json,
        embed("quiz"),
        merge(quiz),
        jinja_template("prompts/review_quiz.jinja"),
        chat_fn,
        debug,
    )
    chain_fn(quiz)


if __name__ == "__main__":
    main()
