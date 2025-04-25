from typing import Any


def transform(data: list[dict[str, Any]]) -> list[int]:
    return list(
        map(
            lambda x: x["a"]["b"].get("c", {}).get("d", 0) + 5 if x["flag"] else -1,
            data,
        )
    )


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
