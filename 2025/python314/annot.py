import annotationlib

# You no longer need string annotations or `from __future__ import annotations`
class Node:
    def __init__(self, value: int, next: Node | None = None):  # This works fine in Python 3.14
        self.value = value
        self.next = next

def my_function(x: int, y: Node | None) -> bool:
    return x > 0 and y is not None

def main() -> None:
    sig = annotationlib.get_annotations(my_function)
    print(sig)

if __name__ == "__main__":
    main()
