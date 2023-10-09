from typing import Callable


def base_operation1() -> None:
    print("Base operation1")


def base_operation2() -> None:
    print("Base operation2")


def base_operation3() -> None:
    print("Base operation3")


def template_method(
    required_operations1: Callable[[], None],
    required_operations2: Callable[[], None],
    hook1: Callable[[], bool] = lambda: True,
    hook2: Callable[[], None] = lambda: None,
) -> None:
    base_operation1()
    required_operations1()
    base_operation2()
    if hook1():
        base_operation3()
    hook2()
    required_operations2()


def operation1_impl() -> None:
    print("Implemented Operation1")


def operation2_impl() -> None:
    print("Implemented Operation2")


def overridden_hook1() -> bool:
    print("Overridden Hook1")
    return False


def main() -> None:
    # Using default hooks
    template_method(operation1_impl, operation2_impl)

    # Overriding hook1
    template_method(operation1_impl, operation2_impl, overridden_hook1)


if __name__ == "__main__":
    main()
