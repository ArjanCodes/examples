import json
from typing import Any, Type

from pydantic import BaseModel

from ai_utils import (
    call_llm,
    extract_structured_dict,
)


def format_history(history: list[dict[str, str]]) -> str:
    return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history)


def ask_next_question(
    accumulated: dict[str, Any],
    history: list[dict[str, str]],
) -> str:
    instructions = (
        "Given the conversation history and partially filled data,\n"
        "ask ONE question about a field that is still null.\n"
        "Do NOT answer the question yourself.\n"
        "Respond ONLY with the question."
    )

    context = (
        format_history(history)
        + "\n\nCurrent field values:\n"
        + json.dumps(accumulated)
    )

    return call_llm(
        instructions=instructions,
        context=context,
    )


def run_declarative_flow(
    model_type: Type[BaseModel],
    domain_instructions: str,
    debug: bool = True,
) -> BaseModel:
    print("=== Declarative LLM Data Collection ===\n")

    field_names = list(model_type.model_fields.keys())
    accumulated = {f: None for f in field_names}

    history = [
        {
            "role": "system",
            "content": (
                domain_instructions.strip() + "\n\n"
                "You are collecting structured data.\n"
                "Rules:\n"
                "- Ask one question at a time.\n"
                "- Only ask about missing fields.\n"
                "- Never answer your own question.\n"
                "- Never guess values.\n"
                "- Stop when all fields are filled.\n"
            ),
        }
    ]

    def log(*args):
        if debug:
            print("[DEBUG]", *args)

    def complete() -> bool:
        return all(v is not None for v in accumulated.values())

    # -------------------------------------------------------
    # Main loop
    # -------------------------------------------------------
    while not complete():
        log("ACCUMULATED BEFORE:", accumulated)

        # 1. LLM chooses next field → question
        question = ask_next_question(
            accumulated=accumulated,
            history=history,
        )
        print(f"Assistant: {question}")
        history.append({"role": "assistant", "content": question})

        # 2. User answers
        user_answer = input("You: ")
        history.append({"role": "user", "content": user_answer})

        # 3. Extract the information
        partial = extract_structured_dict(
            model_type=model_type,
            user_answer=user_answer,
            context=format_history(history),
            allowed_fields=field_names,
        )

        # 4. Merge into accumulator
        for k, v in partial.items():
            accumulated[k] = v

        log("ACCUMULATED AFTER:", accumulated)
        print()

    # Validate final Pydantic model
    return model_type(**accumulated)
