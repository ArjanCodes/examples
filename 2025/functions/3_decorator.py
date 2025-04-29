from functools import wraps
from typing import Any, Callable


def print_result(
    fmt: str = "Result: {}",
) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(x: Any) -> Any:
            result = func(x)
            print(fmt.format(result))
            return result

        return wrapper

    return decorator


@print_result(fmt="Computed value => {}")
def double(x: int) -> int:
    return x * 2


def main() -> None:
    double(5)


if __name__ == "__main__":
    main()
