import random
import time
from typing import Callable

import httpx


def retry[T](operations: list[Callable[[], T]], delay: float = 1.0) -> T:
    """Retry an operation several times before failing."""
    for attempt, operation in enumerate(operations):
        try:
            return operation()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(delay)


def fetch_backup_api() -> str:
    """Fallback if the main API fails."""
    return "Backup API: Chuck Norris can delete the Recycle Bin."


def fetch_main_api() -> str:
    """Fetch from the main Chuck Norris API."""
    # randomly raise an error to simulate failures
    if random.random() < 0.8:
        raise RuntimeError("simulated random failure")
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random", timeout=2.0)
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return data["value"]


def get_joke() -> str:
    return retry([fetch_main_api] * 3 + [fetch_backup_api])


def main() -> None:
    print(get_joke())


if __name__ == "__main__":
    main()
