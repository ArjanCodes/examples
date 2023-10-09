from typing import Callable


def update_observer1(value: str) -> None:
    print(f"Observer 1 received {value}")


def update_observer2(value: str) -> None:
    print(f"Observer 2 received {value}")


UpdateFn = Callable[[str], None]


def notify(update_fns: list[UpdateFn], value: str):
    for update_fn in update_fns:
        update_fn(value)


def main() -> None:
    update_fns = [update_observer1, update_observer2]
    notify(update_fns, "Some data")


if __name__ == "__main__":
    main()
