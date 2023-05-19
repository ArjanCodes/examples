from dataclasses import dataclass
from typing import Generic, Self, TypeVar

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    next: Self | None = None


@dataclass
class CustomList(Generic[T]):
    head: Node[T] | None = None
    tail: Node[T] | None = None
    length: int = 0

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> T:
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        current = self.head
        for _ in range(index):
            current = current.next
        return current.value

    def __setitem__(self, index: int, value: T) -> None:
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        current = self.head
        for _ in range(index):
            current = current.next
        current.value = value

    def append(self, item: T) -> None:
        new_node = Node(item)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def remove(self, item: T) -> None:
        current = self.head
        previous = None
        found = False

        while current and not found:
            if current.value == item:
                found = True
            else:
                previous = current
                current = current.next

        if not found:
            raise ValueError("Item not found")

        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

        if current == self.tail:
            self.tail = previous

        self.length -= 1

    def count(self, item: T) -> int:
        count = 0
        current = self.head

        while current:
            if current.value == item:
                count += 1
            current = current.next

        return count

    def unique(self) -> list[T]:
        unique_items = set()
        current = self.head

        while current:
            unique_items.add(current.value)
            current = current.next

        return list(unique_items)


def main() -> None:
    # Create a CustomList instance
    my_list = CustomList[int]()

    # Append elements to the list
    my_list.append(10)
    my_list.append(20)
    my_list.append(30)

    # Access elements using indexing
    print(my_list[0])  # Output: 10
    print(my_list[1])  # Output: 20

    # Modify an element
    my_list[1] = 25
    print(my_list[1])  # Output: 25

    # Get the length of the list
    print(len(my_list))  # Output: 3

    # Remove an element
    my_list.remove(10)
    print(len(my_list))  # Output: 2

    # Count occurrences of an element
    my_list.append(25)
    my_list.append(25)
    count = my_list.count(25)
    print(count)  # Output: 3

    # Get unique elements
    unique_items = my_list.unique()
    print(unique_items)  # Output: [25]


if __name__ == "__main__":
    main()
