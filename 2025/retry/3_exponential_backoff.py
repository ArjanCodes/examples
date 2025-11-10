import random
import time

import httpx


def retry(operation, retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Retry an operation using exponential backoff."""
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise
            sleep_time = delay * (backoff ** (attempt - 1))
            print(f"Retrying in {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)


def fetch_joke() -> str:
    """Fetch a random Chuck Norris joke."""
    # randomly raise an error to simulate failures
    if random.random() < 0.5:
        raise RuntimeError("simulated random failure")
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random", timeout=2.0)
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return data["value"]


def main() -> None:
    joke: str = retry(fetch_joke, retries=3, delay=1.0, backoff=2.0)
    print(joke)


if __name__ == "__main__":
    main()
