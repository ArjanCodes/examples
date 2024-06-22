import json
from typing import Any


def parse_json(data: str) -> Any:
    # trim characters until you reach the first { or [
    start = data.find("{")
    if start == -1:
        start = data.find("[")
    data = data[start:]

    # trim characters from the right until you reach a } or ]
    end = data.rfind("}")
    if end == -1:
        end = data.rfind("]")
    data = data[: end + 1]

    return json.loads(data)
