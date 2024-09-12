from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node | None" = None
    prev: "Node | None" = None


def main() -> None:
    # Create two nodes
    node1 = Node(10)
    node2 = Node(20)

    # Create a circular reference
    node1.next = node2
    node2.prev = node1

    # Creating circular references between node1 and node2
    node2.next = node1
    node1.prev = node2

    # Delete the references
    del node1
    del node2


if __name__ == "__main__":
    main()
