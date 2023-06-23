import os

import json
from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMPT_COUNTRY_INFO = """
    You are a RESTful API that only responds in JSON.
    Tell me what the capital is of {country}. If you don't know the country, make up a capital name.
    The JSON response should an object with a field called "capital" containing the capital of the country.
    """


def to_json(json_str: str) -> object:
    cleaned_json = json_str.strip().replace('\\"', "'").replace("\\", "\\\\")
    try:
        return json.loads(cleaned_json)
    except json.decoder.JSONDecodeError as err:
        print("JSONDecodeError: ", err)
        print("+++++++++++++++")
        print(cleaned_json)
        print("+++++++++++++++")
        return {}


def main():
    # setup the chat model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)
    message = HumanMessagePromptTemplate.from_template(template=PROMPT_COUNTRY_INFO)
    chat_prompt = ChatPromptTemplate.from_messages([message])

    # get user input
    country = input("Enter the name of a country: ")

    # generate the response
    print("Generating response...")
    chat_prompt_with_values = chat_prompt.format_prompt(country=country)
    result = llm(chat_prompt_with_values.to_messages())
    json_data: dict[str, Any] = to_json(result.content)

    # print the response
    print(json_data)
    capital = json_data.get("capital", "Unknown")
    print(f"The capital of {country} is {capital}.")


if __name__ == "__main__":
    main()
