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


# Needs timestamp argment needs to be passed either way
# While level does not need to be passed

# def log_message(message: str, timestamp: str | None, level: str = "INFO") -> str:
#     # If no timestamp is provided, use the current time
#     if timestamp is None:
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     # Create the log message with the level and timestamp
#     log_entry = f"[{timestamp}] [{level}] {message}"
#     return log_entry


def log_message(message: str, timestamp: str | None = None, level: str = "INFO") -> str:
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    return log_entry


def main() -> None:
	_log1 = log_message("System started.")
	_log2 = log_message("User logged in", "2024-08-27 12:00:00", "WARNING")
	_log3 = log_message("File not found", level="ERROR")
     

if __name__ == "__main__":
    main()