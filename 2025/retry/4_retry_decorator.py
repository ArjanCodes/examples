import random
import time
from functools import wraps
from typing import Any, Callable

import httpx


def retry_decorator[T](
    retries: int = 3, delay: float = 1.0, backoff: float = 2.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """A decorator that retries the wrapped function on failure."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        raise
                    sleep_time = delay * (backoff ** (attempt - 1))
                    print(f"Retrying in {sleep_time:.1f} seconds...")
                    time.sleep(sleep_time)
            raise RuntimeError("All retries failed")

        return wrapper

    return decorator


@retry_decorator(retries=4, delay=1.0)
def fetch_joke() -> str:
    """Fetch a random Chuck Norris joke."""
    # randomly raise an error to simulate failures
    if random.random() < 0.5:
        raise RuntimeError("simulated random failure")
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random", timeout=2.0)
        response.raise_for_status()
        return response.json()["value"]


def main() -> None:
    print(fetch_joke())


if __name__ == "__main__":
    main()
