import random
import string
from dataclasses import dataclass, field
from enum import StrEnum, auto


class Brand(StrEnum):
    """Represents a vehicle brand."""

    VOLKSWAGEN_ID3 = auto()
    BMW_5 = auto()
    TESLA_MODEL_3 = auto()
    TESLA_MODEL_5 = auto()


@dataclass
class VehicleInfo:
    brand: Brand
    electric: bool
    catalogue_price: int

    @property
    def tax(self) -> float:
        tax_percentage = 0.02 if self.electric else 0.05
        return tax_percentage * self.catalogue_price

    def print(self) -> None:
        print(f"Brand: {self.brand}")
        print(f"Payable tax: {self.tax}")


@dataclass
class Vehicle:
    id: str
    license_plate: str
    info: VehicleInfo

    def print(self):
        print(f"Id: {self.id}")
        print(f"License plate: {self.license_plate}")
        self.info.print()


@dataclass
class VehicleRegistry:
    vehicle_info: dict[Brand, VehicleInfo] = field(default_factory=dict)

    def __post_init__(self):
        self.add_vehicle_info(Brand.TESLA_MODEL_3, True, 60_000)
        self.add_vehicle_info(Brand.VOLKSWAGEN_ID3, True, 35_000)
        self.add_vehicle_info(Brand.BMW_5, False, 45_000)
        self.add_vehicle_info(Brand.TESLA_MODEL_5, True, 75_000)

    def add_vehicle_info(
        self, brand: Brand, electric: bool, catalogue_price: int
    ) -> None:
        self.vehicle_info[brand] = VehicleInfo(brand, electric, catalogue_price)

    def generate_vehicle_id(self, length: int) -> str:
        return "".join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id: str) -> str:
        first_two_digits = id[:2]
        middle_two_digits = "".join(random.choices(string.digits, k=2))
        last_two_digits = "".join(random.choices(string.ascii_uppercase, k=2))

        return f"{first_two_digits}-{middle_two_digits}-{last_two_digits}"

    def create_vehicle(self, brand: Brand) -> Vehicle:
        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, self.vehicle_info[brand])


def register_vehicle(brand: Brand):
    registry = VehicleRegistry()
    vehicle = registry.create_vehicle(brand)
    vehicle.print()


def main() -> None:
    register_vehicle(Brand.VOLKSWAGEN_ID3)


if __name__ == "__main__":
    main()
