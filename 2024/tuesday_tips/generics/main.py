from stack import Stack
from numeric_stack import NumericStack


def main() -> None:
    stack = Stack[int]()

    stack.push(1)

    print(f"Stack of ints: {stack}")

    numeric_stack = NumericStack[int]()

    numeric_stack.push(1)

    print(f"Vector of ints: {numeric_stack}")


if __name__ == "__main__":
    main()
