from typing import Self

# ============================================================
# 3) Non-data descriptor (only __get__) can be shadowed
# ============================================================


class NonData:
    def __get__(self, instance: object | None, owner: type) -> str | Self:
        if instance is None:
            return self
        return "from descriptor"


class A:
    x: NonData = NonData()


# ============================================================
# 4) Data descriptor (has __set__) cannot be shadowed
# ============================================================


class Data:
    def __get__(self, instance: object | None, owner: type) -> str | Self:
        if instance is None:
            return self
        return "from descriptor"

    def __set__(self, instance: object, value: str) -> None:
        instance.__dict__["x"] = value


class B:
    x: Data = Data()


def main() -> None:

    a = A()
    print(a.x)
    a.__dict__["x"] = "from instance dict"
    print(a.x)  # shadowed by instance dict

    b = B()
    b.__dict__["x"] = "from instance dict"
    print(b.x)  # descriptor still wins (data descriptor precedence)


if __name__ == "__main__":
    main()
