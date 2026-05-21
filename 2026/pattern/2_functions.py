from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


@dataclass(frozen=True)
class Summary:
    text: str
    model: str
    tokens_used: int


PromptBuilder = Callable[[str], str]


def concise_prompt(text: str) -> str:
    return f"Summarize this in one concise paragraph:\n\n{text}"


def bullet_prompt(text: str) -> str:
    return f"Summarize this as bullet points:\n\n{text}"


PROMPTS: dict[str, PromptBuilder] = {
    "concise": concise_prompt,
    "bullets": bullet_prompt,
}


def build_prompt(style: str, text: str) -> str:
    try:
        return PROMPTS[style](text)
    except KeyError:
        raise ValueError(f"Unknown style: {style}") from None


def fake_call_llm(prompt: str) -> LLMResponse:
    return LLMResponse(
        text=f"Summary of: {prompt[:60]}...",
        input_tokens=len(prompt.split()),
        output_tokens=40,
        model="fake-model",
    )


def split_into_chunks(text: str) -> list[str]:
    return [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]


def summarize_document(text: str, style: str) -> Summary:
    chunks = split_into_chunks(text)

    partial_summaries = [
        fake_call_llm(build_prompt(style, chunk)).text for chunk in chunks
    ]

    final_response = fake_call_llm(build_prompt(style, "\n\n".join(partial_summaries)))

    return Summary(
        text=final_response.text,
        model=final_response.model,
        tokens_used=final_response.input_tokens + final_response.output_tokens,
    )


def main() -> None:
    document = """
    Python code often becomes harder to maintain when abstractions are added too early.

    Design patterns can help, but only when they remove real complexity.
    """

    summary = summarize_document(document, style="bullets")
    print(summary)


if __name__ == "__main__":
    main()
