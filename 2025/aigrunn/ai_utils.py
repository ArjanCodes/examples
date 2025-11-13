import json
import os
from typing import Any, Type

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# -------------------------------------------------------------------
# API key and LLM settings
# -------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=API_KEY)

LLM_MODEL = "gpt-5-mini"


# -------------------------------------------------------------------
# Base wrapper — ALL LLM CALLS go through this
# -------------------------------------------------------------------
def call_llm(
    *,
    instructions: str,
    context: str,
) -> str:
    """
    Low-level unified LLM wrapper.
    Sends instructions + context and returns raw assistant text.
    """
    response = client.responses.create(
        model=LLM_MODEL,
        instructions=instructions,
        input=context,
    )
    return response.output_text.strip()


# -------------------------------------------------------------------
# Extract JSON object from LLM text
# -------------------------------------------------------------------
def extract_json_object(text: str) -> str:
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return text[start : end + 1]

    raise ValueError(f"LLM did not return JSON:\n{text}")


# -------------------------------------------------------------------
# Universal structured extractor (built on call_llm)
# -------------------------------------------------------------------
def extract_structured_dict(
    *,
    model_type: Type[BaseModel],
    user_answer: str,
    context: str | None = None,
    allowed_fields: list[str] | None = None,
) -> dict[str, Any]:
    """
    Universal structured extraction. Always returns a dict.
    """

    schema = model_type.model_json_schema()

    allowed = ""
    if allowed_fields:
        allowed_keys = ", ".join(f'"{f}"' for f in allowed_fields)
        allowed = f"Valid JSON keys: {allowed_keys}\n"

    instructions = f"""
Respond strictly with a JSON object matching this schema:

{schema}

Rules:
- Extract ONLY fields explicitly stated by the user.
- Do NOT guess values.
- Do NOT output missing fields.
- {allowed}
- Convert yes/no into true/false when appropriate.
- Respond ONLY with valid JSON. No explanation or markdown.
"""

    ctx = (
        f"{context}\n\nUser answer: {user_answer}"
        if context
        else f"User answer: {user_answer}"
    )

    raw = call_llm(
        instructions=instructions,
        context=ctx,
    )

    json_text = extract_json_object(raw)
    return json.loads(json_text)
