from stack import Stack
from vector_stack import VectorStack


def main() -> None:
    stack = Stack[int]()

    stack.push(1)

    print(f"Stack of ints: {stack}")

    vector_stack = VectorStack[int]()

    vector_stack.push(1)

    print(f"Vector of ints: {vector_stack}")


if __name__ == "__main__":
    main()
