import os
import openai
from openai import AuthenticationError, OpenAI
from logging import getLogger
from dotenv import load_dotenv

logger = getLogger(__name__)

load_dotenv()


def initiate_client(api_key: str) -> OpenAI:
    logger.info("Initiating client")

    if not check_validity(api_key):
        logger.error("Invalid API key.")
        raise ValueError("Invalid API key.")

    return OpenAI(api_key=api_key)


def check_validity(api_key: str) -> bool:
    logger.info("Checking validity of API key")
    try:
        openai.api_key = api_key
        openai.models.list()
    except AuthenticationError as _e:
        return False
    return True


def main():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        logger.error("Cannot initiate OpenAI client, please provide an API key.")
        raise ValueError("Cannot initiate OpenAI client, please provide an API key.")

    initiate_client(api_key)
