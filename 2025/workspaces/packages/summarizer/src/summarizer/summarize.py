from openai import OpenAI

def summarize_text(text: str, api_key: str) -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )

    response = client.responses.create(
        model="gpt-5",
        instructions="You are a text summary writer.",
        input=f"Summarize the following text into a single concise paragraph: {text}"
    )

    return response.output_text