import tiktoken
from models import OpenAIModels


def get_number_of_tokens(text: str, model: OpenAIModels) -> int:
    encoding = tiktoken.get_encoding("cl100k_base") # This is going to be an problem, better if we can store it in the Enum

    tokens = encoding.encode(text)

    return len(tokens)
