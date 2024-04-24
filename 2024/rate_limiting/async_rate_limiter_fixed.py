import asyncio
import functools
import time
import typing


def rate_limited[
** P, R
](seconds_between_calls: float, global_limit: bool = True) -> typing.Callable[
    [typing.Callable[P, typing.Awaitable[R]]], typing.Callable[P, typing.Awaitable[R]]
]:
    last_time_called = 0.0
    lock = asyncio.Lock()

    def decorator(func: typing.Callable[P, typing.Awaitable[R]]) -> typing.Callable[P, typing.Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal last_time_called
            async with lock:
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = seconds_between_calls - elapsed
                if left_to_wait > 0:
                    await asyncio.sleep(left_to_wait)
                result = await func(*args, **kwargs)
                last_time_called = time.perf_counter()
            return result

        if global_limit:
            return wrapper
        else:
            return decorator(func)

    return decorator


@rate_limited(3.0)
async def example() -> None:
    print("hello")


async def not_limited() -> None:
    print("not limited")


async def main() -> None:
    tasks = []
    for _ in range(10):
        tasks.append(asyncio.create_task(example()))
        tasks.append(asyncio.create_task(not_limited()))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
