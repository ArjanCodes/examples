from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps


@dataclass(frozen=True)
class AccountData:
    email: str


@dataclass(frozen=True)
class Account:
    id: int
    email: str


def audit[**P, T](function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("audit: creating account")
        result = function(*args, **kwargs)
        print("audit: account created")
        return result

    return wrapper


def retry[**P, T](max_attempts: int) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"retry: attempt {attempt}")
                    return function(*args, **kwargs)
                except RuntimeError:
                    if attempt == max_attempts:
                        raise

            raise AssertionError("Unreachable")

        return wrapper

    return decorate


def transactional[**P, T](function: Callable[P, T]) -> Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print("transaction: begin")
        try:
            result = function(*args, **kwargs)
        except Exception:
            print("transaction: rollback")
            raise
        print("transaction: commit")
        return result

    return wrapper


def require_permission[**P, T](permission: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            print(f"permission: checked {permission}")
            return function(*args, **kwargs)

        return wrapper

    return decorate


@audit
@retry(max_attempts=3)
@transactional
@require_permission("accounts:create")
def create_account(data: AccountData) -> Account:
    print(f"repository: inserted {data.email}")
    return Account(id=1, email=data.email)


def main() -> None:
    account = create_account(AccountData(email="ada@example.com"))
    print(f"Created account {account.id}")


if __name__ == "__main__":
    main()
