import asyncio
import logging
from file_handler import read_file
from client import initialize__async_openai_client
from models import OpenAIModels
from dotenv import load_dotenv

from tip_3.request_handler import handle_request


load_dotenv()


async def main() -> None:
    client = initialize__async_openai_client()

    query = read_file("./files/short_story.txt")

    tasks = [
        handle_request(query=query, model=model, client=client)
        for model in OpenAIModels
    ]

    result: list[str] = await asyncio.gather(*tasks)

    print(result)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    asyncio.run(main())
