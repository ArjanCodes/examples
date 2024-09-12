from math import fma
from pathlib import Path
from re import PatternError, compile
from typing import Protocol, ReadOnly, TypedDict, is_protocol


class MyProtocol(Protocol):
    def some_method(self) -> int: ...


class Point2D(TypedDict):
    x: float
    y: float
    label: ReadOnly[str]


def main() -> None:
    print(fma(1, 2, 3))  # 1 * 2 + 3 = 5

    # test re pattern error
    try:
        compile("[a-")  # Missing closing bracket
    except PatternError as e:
        print(e)

    # create path from file URI
    p = Path.from_uri("file:///home/user/file.txt")
    print(p)

    # create a point
    point = Point2D(x=10, y=20, label="A")
    print(point)
    point["label"] = "hello"  # type checker error

    # check if MyProtocol is a protocol
    print(is_protocol(MyProtocol))
    print(is_protocol(Point2D))


if __name__ == "__main__":
    main()
