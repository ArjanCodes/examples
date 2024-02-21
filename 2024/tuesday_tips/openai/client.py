import os
from openai import AsyncOpenAI, OpenAI


SYSTEM_MESSAGE =  "You are an translation tool that always translate to dutch"
        
def initialize_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set your OPENAI_API_KEY in the .env file.")

    return OpenAI(api_key=api_key)

def initialize__async_openai_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set your OPENAI_API_KEY in the .env file.")

    return AsyncOpenAI(api_key=api_key)


