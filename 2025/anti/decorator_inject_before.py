import json
from functools import wraps
from typing import Any, Callable


def load_config(file_name: str) -> dict[str, Any]:
    """Load configuration from the specified file."""
    with open(file_name, "r") as f:
        return json.load(f)


def inject_config(file_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            config: dict[str, Any] = load_config(file_name)
            return func(config, *args, **kwargs)

        return wrapper

    return decorator


@inject_config("config.json")
def main(config: dict[str, Any]) -> None:
    print(f"Training with config: {config}")


if __name__ == "__main__":
    main()
