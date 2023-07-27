import os

from langchain.chat_models import ChatOpenAI
from langchain.chains.api import open_meteo_docs
from langchain.chains import APIChain
from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def main():
    # setup the chat model
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

    chain_new = APIChain.from_llm_and_api_docs(
        llm, open_meteo_docs.OPEN_METEO_DOCS, verbose=False
    )

    result = chain_new.run(
        "What is the weather like right now in Amsterdam, The Netherlands in degrees Celcius?"
    )
    print(result)


if __name__ == "__main__":
    main()
