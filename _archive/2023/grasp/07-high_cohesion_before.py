import random
import string
from enum import StrEnum, auto


class Brand(StrEnum):
    """Represents a vehicle brand."""

    VOLKSWAGEN_ID3 = auto()
    BMW_5 = auto()
    TESLA_MODEL_3 = auto()


class VehicleRegistry:
    """Registration of vehicle in the system."""

    def generate_vehicle_id(self, length: int) -> str:
        """Generates a random vehicle id."""
        return "".join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id: str) -> str:
        """Generates a random vehicle license plate."""
        first_two_digits = id[:2]
        middle_two_digits = "".join(random.choices(string.digits, k=2))
        last_two_digits = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{first_two_digits}-{middle_two_digits}-{last_two_digits}"


def register_vehicle(brand: Brand) -> None:

    registry = VehicleRegistry()

    vehicle_id = registry.generate_vehicle_id(12)

    license_plate = registry.generate_vehicle_license(vehicle_id)

    catalogue_price = 0
    if brand == Brand.TESLA_MODEL_3:
        catalogue_price = 60000
    elif brand == Brand.VOLKSWAGEN_ID3:
        catalogue_price = 35000
    elif brand == Brand.BMW_5:
        catalogue_price = 45000

    tax_percentage = 0.05
    if brand in [Brand.TESLA_MODEL_3, Brand.VOLKSWAGEN_ID3]:
        tax_percentage = 0.02

    payable_tax = tax_percentage * catalogue_price

    print("Registration complete. Vehicle information:")
    print(f"Brand: {brand.name}")
    print(f"Id: {vehicle_id}")
    print(f"License plate: {license_plate}")
    print(f"Payable tax: {payable_tax}")


def main() -> None:
    register_vehicle(Brand.VOLKSWAGEN_ID3)


if __name__ == "__main__":
    main()
