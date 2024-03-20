import time
from typing import Any, Callable


def timer_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"{func.__name__} with input {args[-1]} took {end_time - start_time:.5f} seconds to execute."
        )
        return result

    return wrapper
