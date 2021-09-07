import functools
from typing import Callable

ComposableFunction = Callable[[float], float]

# Helper function for composing functions
def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def addThree(x: float) -> float:
    return x + 3


def multiplyByTwo(x: float) -> float:
    return x * 2


def addN(n: float) -> ComposableFunction:
    return lambda x: x + n


def main():
    x = 12
    # oldres = multiplyByTwo(multiplyByTwo(addThree(addThree(x))))
    myfunc = compose(addN(3), addN(3), multiplyByTwo, multiplyByTwo)
    result = myfunc(x)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
