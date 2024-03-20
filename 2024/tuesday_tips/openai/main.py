from file_handler import read_file
from client import initialize_openai_client
from models import OpenAIModels
from dotenv import load_dotenv

from tip_1.request_handler import handle_request

load_dotenv()


def main() -> None:
    client = initialize_openai_client()

    model = OpenAIModels.GPT4

    query = read_file("./files/short_story.txt")

    result = handle_request(query=query, model=model, client=client)

    print(result)


if __name__ == "__main__":
    main()
