import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()  # Loads the .env file into the program so we can access the enviroment variables with getenv()

SECRET_KEY = os.getenv("SECRET_KEY", "siekret")


def main():
    client = OpenAI(api_key=SECRET_KEY)

    prompt = "What is the best way to store credentials?"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a assistant to arjancodes, skilled in software design patterns with creative flair. And likes to end your sentences with an swedish joke",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    print(completion.choices[0].message)


if __name__ == "__main__":
    main()
