from typing import Callable

from openai import OpenAI

# Models
GPT3_TURBO = "gpt-3.5-turbo"
GPT4 = "gpt-4o"
GPT4_MINI = "gpt-4o-mini"

type ChatFn = Callable[[str], str]


def chatter(api_key: str, model: str = GPT4_MINI) -> ChatFn:
    ai_client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": "You are a key-value store. Whevener I mention a UUID, respond with the data associated with that UUID.",
        }
    ]

    def send_chat_request(query: str) -> str:
        messages.append({"role": "user", "content": query})
        response = ai_client.chat.completions.create(
            model=model,
            messages=messages,
        )
        chat_result = response.choices[0].message.content
        if not chat_result:
            raise ValueError("No response from the chat model.")
        return chat_result

    return send_chat_request
