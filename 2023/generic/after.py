class Box[T]:
    def __init__(self, item: T):
        self.item = item

    def get_item(self) -> T:
        return self.item

    def set_item(self, new_item: T) -> None:
        self.item = new_item


# For integers
int_box = Box(123)
int_item: int = int_box.get_item()
print(int_item)  # Outputs: 123

# For strings
str_box = Box("Hello, Generics!")
str_item: str = str_box.get_item()
print(str_item)  # Outputs: Hello, Generics!
