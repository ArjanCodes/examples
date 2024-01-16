import time
from functools import wraps
from typing import Any, Callable

def rate_limit(max_calls: int, period: float = 1.0) -> Callable[[Any], Any]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        timestamps: list[float] = []

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any)-> Any:

            now = time.time()
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) < max_calls:
                timestamps.append(now)
                return func(*args, **kwargs)
            else:
                wait = period - (now - timestamps[0])
                print(f"Rate limit achieved, wait. {wait}")
                time.sleep(wait)
                return wrapper(*args, **kwargs)

        return wrapper
    return decorator