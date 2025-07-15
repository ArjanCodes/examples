from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True


def main():
    product = Product(name="Widget", price=19.99)
    print(product)


if __name__ == "__main__":
    main()
