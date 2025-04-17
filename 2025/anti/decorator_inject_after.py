import json
from typing import Any


def load_config(file_name: str) -> dict[str, Any]:
    """Load configuration from the specified file."""
    with open(file_name, "r") as f:
        return json.load(f)


def main() -> None:
    config = load_config("config.json")
    print(f"Training with config: {config}")


if __name__ == "__main__":
    main()
