def compute_total_price(unit_price: int, quantity: int = 1, discount_perc: float = 0):
    total = unit_price * quantity
    return int((1 - discount_perc) * total)


def oops(my_list: list[int] = []):
    my_list.append(30)
    return my_list


def main():
    price = 340_00
    discount = 0.15
    print(
        f"Total price minus discount: ${compute_total_price(unit_price=price, discount_perc=discount) / 100:.2f}"
    )

    print(oops())
    print(oops())  # prints [30, 30] -> oops!


if __name__ == "__main__":
    main()
