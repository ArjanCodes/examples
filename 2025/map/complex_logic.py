from typing import Any


def transform(data: list[dict[str, Any]]) -> list[int]:
    result: list[int] = []
    for item in data:
        if item["flag"]:
            try:
                val = item["a"]["b"].get("c", {}).get("d", 0)
                result.append(val + 5)
            except KeyError:
                result.append(-1)
        else:
            result.append(-1)
    return result


def main() -> None:
    data: list[dict[str, Any]] = [
        {"flag": True, "a": {"b": {"c": {"d": 1}}}},
        {"flag": False, "a": {"b": {"c": {"d": 2}}}},
        {"flag": True, "a": {"b": {"c": {}}}},
        {"flag": True, "a": {"b": {}}},
    ]

    result = transform(data)
    print(result)  # Output: [6, -1, 5, 5]


if __name__ == "__main__":
    main()
