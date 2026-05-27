from final import LLMResponse, summarize_document


class FakeLLMClient:
    def generate(self, prompt: str) -> LLMResponse:

        return LLMResponse(
            text=f"Summary: {prompt[:30]}",
            input_tokens=10,
            output_tokens=5,
            model="fake-model",
        )

    def count_tokens(self, text: str) -> int:

        return len(text.split())

    def max_context_window(self) -> int:

        return 1_000


def test_summarize_document() -> None:

    summary = summarize_document(
        text="""

        Python code often becomes harder to maintain when abstractions are added too early.

        Design patterns can help, but only when they remove real complexity.

        """,
        style="concise",
        llm=FakeLLMClient(),
    )

    assert summary.text.startswith("Summary:")

    assert summary.model == "fake-model"

    assert summary.tokens_used > 0
