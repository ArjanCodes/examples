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


def count_tokens(text: str) -> int:
    return len(text.split())


def call_llm(prompt: str) -> LLMResponse:
    return LLMResponse(
        text=f"Summary of: {prompt[:60]}...",
        input_tokens=count_tokens(prompt),
        output_tokens=40,
        model="fake-model",
    )


def split_into_chunks(
    text: str,
    max_tokens: int,
    count_tokens: Callable[[str], int],
) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []

    for paragraph in paragraphs:
        candidate = "\n\n".join([*current, paragraph])

        if count_tokens(candidate) <= max_tokens:
            current.append(paragraph)
        else:
            chunks.append("\n\n".join(current))
            current = [paragraph]

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def summarize_document(text: str, style: str) -> Summary:
    chunks = split_into_chunks(
        text,
        max_tokens=500,
        count_tokens=count_tokens,
    )

    partial_summaries: list[str] = []
    tokens_used = 0

    for chunk in chunks:
        response = call_llm(build_prompt(style, chunk))
        partial_summaries.append(response.text)
        tokens_used += response.input_tokens + response.output_tokens

    final_response = call_llm(build_prompt(style, "\n\n".join(partial_summaries)))

    tokens_used += final_response.input_tokens + final_response.output_tokens

    return Summary(
        text=final_response.text,
        model=final_response.model,
        tokens_used=tokens_used,
    )


def main() -> None:
    document = """
    Python code often becomes harder to maintain when abstractions are added too early.

    Design patterns can help, but only when they remove real complexity.
    """

    summary = summarize_document(document, style="concise")
    print(summary)


if __name__ == "__main__":
    main()
