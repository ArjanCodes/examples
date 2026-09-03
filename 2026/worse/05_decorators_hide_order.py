from collections.abc import Callable
from functools import wraps


def log_call[**P, T](function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("log: before")
        result = function(*args, **kwargs)
        print("log: after")
        return result

    return wrapper


def require_authorization[**P, T](function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("authorization: checked")
        return function(*args, **kwargs)

    return wrapper


@log_call
@require_authorization
def delete_project(project_id: int) -> None:
    print(f"deleted project {project_id}")


def main() -> None:
    # Decorators apply bottom-up: log_call wraps require_authorization.
    delete_project(42)


if __name__ == "__main__":
    main()
