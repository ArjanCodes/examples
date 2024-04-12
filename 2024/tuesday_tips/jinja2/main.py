import os

from chat import chatter
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_KEY")
    if not openai_api_key:
        raise ValueError(
            "No API key found. Please set your OPENAI_KEY in the .env file."
        )

    chat = chatter(api_key=openai_api_key)

    response = chat("What is the capital of The Netherlands?")
    print(response)


if __name__ == "__main__":
    main()
