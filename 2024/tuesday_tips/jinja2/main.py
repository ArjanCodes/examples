import os

from chat import GPT3_TURBO, chatter
from dotenv import load_dotenv
from jinja_helper import process_template

load_dotenv()


def main() -> None:
    api_key = os.getenv("OPENAI_KEY")
    if not api_key:
        raise ValueError(
            "No API key found. Please set your OPENAI_KEY in the .env file."
        )
    chat_fn = chatter(api_key)

    email = {
        "customer_name": "Sally Smith",
        "product": "Purple Widget",
        "similar_product": "Orange Widget",
        "tone_of_voice": "short and to the point, no fluffy language",
        "ceo_name": "ArjanCodes",
    }

    # create the email
    email_template = process_template("prompts/create_unavailable_email.jinja", email)
    email_v1 = chat_fn(email_template)
    email["email_body"] = email_v1

    print("Email v1:")
    print(email_v1)

    # review the email
    review_template = process_template("prompts/review_email.jinja", email)
    email_v2 = chat_fn(review_template)

    print("Email v2:")
    print(email_v2)


if __name__ == "__main__":
    main()
