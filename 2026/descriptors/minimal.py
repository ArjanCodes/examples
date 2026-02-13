class DemoDescriptor:
    def __get__(self, instance: object | None, owner: type) -> int:
        print(f"__get__ called with instance={instance}, owner={owner.__name__}")
        return 42

    def __set__(self, instance: object, value: int) -> None:
        print(f"__set__ called with instance={instance}, value={value}")


class Thing:
    x = DemoDescriptor()


def main() -> None:

    t = Thing()

    print(t.x)  # triggers __get__
    t.x = 10  # triggers __set__
    print(Thing.x)  # instance=None


if __name__ == "__main__":
    main()
