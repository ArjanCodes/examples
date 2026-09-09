"""Two typing additions: TypeForm and TypedDict extra_items."""

from typing import Any, TypedDict, TypeForm


class ApiResponse(TypedDict, extra_items=str):
    status: int


def convert[T](type_expression: TypeForm[T], value: Any) -> T:
    """A real library would validate value; TypeForm describes its type argument."""
    return type_expression(value)


def main() -> None:
    response: ApiResponse = {"status": 200, "request_id": "req-123"}
    converted = convert(int, "42")

    # TypeForm is deliberately transparent at runtime.
    print(f"converted: {converted} ({type(converted).__name__})")
    print(f"typed extra item: {response['request_id']}")


if __name__ == "__main__":
    main()
