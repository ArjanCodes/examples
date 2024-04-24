import functools
import time
import typing


def rate_limited[**P, R](seconds_between_calls: float) -> typing.Callable[
    [typing.Callable[P, R]], typing.Callable[P, R]]:
    def decorator(func: typing.Callable[P, R]) -> typing.Callable[P, R]:
        last_time_called = 0.0

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal last_time_called

            elapsed = time.perf_counter() - last_time_called
            left_to_wait = seconds_between_calls - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)

            last_time_called = time.perf_counter()

            return ret

        return wrapper

    return decorator


@rate_limited(1.0)
def example() -> None:
    print("hello")


def main() -> None:
    for _ in range(10):
        example()


if __name__ == "__main__":
    main()
