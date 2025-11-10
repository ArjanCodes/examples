import random
import time
from typing import Callable

import httpx


def retry[T](operation: Callable[[], T], retries: int = 3, delay: float = 1.0) -> T:
    """Retry an operation several times before failing."""
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise
            time.sleep(delay)


def fetch_joke() -> str:
    """Fetch a random Chuck Norris joke from the API."""
    # randomly raise an error to simulate failures
    if random.random() < 0.5:
        raise RuntimeError("simulated random failure")
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random", timeout=2.0)
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return data["value"]


def main() -> None:
    joke: str = retry(fetch_joke, retries=3, delay=1.0)
    print(joke)


if __name__ == "__main__":
    main()
