import logging
import time
from datetime import datetime
from typing import Any

# DO NOT USE mutable default arguments
# Mutable default arguments are evaluated only once when the module is loaded
# This means that the default argument is shared between all calls to the function


def append_to(element: int, to: list[int] = []) -> list[int]:
    to.append(element)
    return to


# DO NOT USE values that need to be calculated during runtime
# In this case, the timestamp should be calculated when the function is called
# But, the timestamp is calculated only once when the module is loaded


def add_timestamp(
    data: dict[str, Any] | None = None, timestamp: float = time.time()
) -> dict[str, Any]:
    """Run the process with the provided timestamp."""
    if data is None:
        data = {}

    data["timestamp"] = timestamp
    return data


def log_message(
    message: str, timestamp: float | None = None, level: str = "INFO"
) -> None:
    # use current time if no timestamp is provided
    if timestamp is None:
        timestamp = time.time()

    # create a string representation of the timestamp
    formatted_ts = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{formatted_ts}] [{level}] {message}")


def main() -> None:
    log_message("System started.")
    log_message("User logged in", timestamp=time.time() - 86400)
    log_message("File not found", level="ERROR")


if __name__ == "__main__":
    main()
