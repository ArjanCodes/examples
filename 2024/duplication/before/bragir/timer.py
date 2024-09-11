import time
from typing import Callable, Any
from bragir.tracing.logger import logger


def timing_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"{func.__name__} elapsed time: {elapsed_time} seconds")
        return result

    return wrapper
