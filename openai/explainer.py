"""OpenAI API controller."""

import os
from functools import partial

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_question(question: str) -> dict:
    """Sendo a question to OpenAI API and gets the response."""
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a developer."},
            {"role": "user", "content": question},
        ],
    )


def retrieve_ai_answer(response: dict) -> str:
    """Isolates the answer message in the AI response."""
    return response["choices"][0]["message"]["content"]


def get_code_info(question: str, code: str) -> str:
    """Gives to the OpenAI API the question to explain a code base."""
    resp = send_question(f"{question} {code}")
    return retrieve_ai_answer(resp)


retrieve_code_language = partial(
    get_code_info, question="Can you explain me in what language was this code written?"
)

retrieve_code_explanation = partial(
    get_code_info, question="Can you explain me what this code base does?"
)
