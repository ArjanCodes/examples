from typing import Callable

from openai import OpenAI

# Models
GPT3_TURBO = "gpt-3.5-turbo"
GPT4_TURBO = "gpt-4-turbo-preview"

type ChatFn = Callable[[str], str]


def chatter(api_key: str, model: str = GPT4_TURBO) -> ChatFn:
    ai_client = OpenAI(api_key=api_key)

    def send_chat_request(query: str) -> str:
        response = ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": query},
            ],
        )
        chat_result = response.choices[0].message.content
        if not chat_result:
            raise ValueError("No response from the chat model.")
        return chat_result

    return send_chat_request
