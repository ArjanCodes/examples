from decimal import Decimal
from typing import Iterable


def add_number_to_each_element(number: int, numbers: list[int]) -> list[int]:
    return [num + number for num in numbers]


def add_number_to_each_element_generic_return(
    number: int, numbers: list[int]
) -> Iterable[int]:
    return [num + number for num in numbers]


# more generic version that also works with other iterables
def add_number_to_each_element_v2(number: int, numbers: Iterable[int]) -> list[int]:
    return [num + number for num in numbers]


# even more generic version that works with any numeric type
def add_number_to_each_element_v3[Numeric: (int, float, Decimal)](
    number: Numeric, numbers: Iterable[Numeric]
) -> list[Numeric]:
    return [num + number for num in numbers]


def main() -> None:
    print(add_number_to_each_element(5, [1, 2, 3, 4, 5]))
    print(add_number_to_each_element_v2(5, [1, 2, 3, 4, 5]))
    print(add_number_to_each_element_v3(5, [1, 2, 3, 4, 5]))
    print(add_number_to_each_element_v3(5.0, [1.0, 2.0, 3.0, 4.0, 5.0]))
    print(
        add_number_to_each_element_v3(
            Decimal("5.0"),
            [
                Decimal("1.0"),
                Decimal("2.0"),
                Decimal("3.0"),
                Decimal("4.0"),
                Decimal("5.0"),
            ],
        )
    )

    generic_return = add_number_to_each_element_generic_return(5, [1, 2, 3, 4, 5])
    # because the return type is Iterable[int], we can't use list methods,
    # so this is limiting
    # print(generic_return[0])
    # generic_return.append(6)


if __name__ == "__main__":
    main()
