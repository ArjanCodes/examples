import logging
from abc import ABC, abstractmethod
from math import sqrt
from time import perf_counter
from typing import Any, Callable


class AbstractDecorator(ABC):
    def __init__(self, decorated: Callable[..., Any]) -> None:
        self._decorated = decorated

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass


class BenchmarkDecorator(AbstractDecorator):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = self._decorated(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(
            f"Execution of {self._decorated.__class__.__name__} took {run_time:.2f} seconds."
        )
        return value


class LoggingDecorator(AbstractDecorator):
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Calling {self._decorated.__class__.__name__}")
        value = self._decorated(*args, **kwargs)
        logging.info(f"Finished {self._decorated.__class__.__name__}")
        return value


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for element in range(2, int(sqrt(number)) + 1):
        if number % element == 0:
            return False
    return True


def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count += 1
    return count


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    benchmark = BenchmarkDecorator(count_prime_numbers)
    with_logging = LoggingDecorator(benchmark)
    with_logging(50000)


if __name__ == "__main__":
    main()
