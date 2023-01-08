import functools
import logging
from math import sqrt
from time import perf_counter
from typing import Any, Callable


def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return value

    return wrapper


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f"Execution of {func.__name__} took {run_time:.2f} seconds.")
        return value

    return wrapper


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for element in range(2, sqrt(number) + 1):
        if number % element == 0:
            return False
    return True


@with_logging
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count += 1
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    count_prime_numbers(50000)


if __name__ == "__main__":
    main()
