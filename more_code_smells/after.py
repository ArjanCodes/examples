"""
Basic example of a Vehicle registration system.
"""
import random
import string
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional

TAX_PERCENTAGE_ELECTRIC = 0.02
TAX_PERCENTAGE_PETROL = 0.05


class RegistryStatus(Enum):
    """Possible statuses for the vehicle registry system."""

    ONLINE = auto()
    CONNECTION_ERROR = auto()
    OFFLINE = auto()


@dataclass
class VehicleInfoMissingError(Exception):
    """Custom error that is raised when vehicle information is missing for a particular brand."""

    brand: str
    model: str
    message: str = "Vehicle information is missing."


@dataclass
class VehicleInfo:
    """Class that contains basic information about a vehicle. Used for registering new vehicles."""

    brand: str
    model: str
    catalogue_price: int
    electric: bool = True
    production_year: int = datetime.now().year

    def compute_tax(self) -> float:
        """Computes the tax to be paid when registering a vehicle of this type."""
        tax_percentage = (
            TAX_PERCENTAGE_ELECTRIC if self.electric else TAX_PERCENTAGE_PETROL
        )
        return tax_percentage * self.catalogue_price

    def __str__(self) -> str:
        tax = self.compute_tax()
        return f"brand: {self.brand} - type: {self.model} - tax: {tax}"


class Vehicle:
    """Class representing a vehicle (electric or fossil fuel)."""

    def __init__(self, vehicle_id: str, license_plate: str, info: VehicleInfo) -> None:
        self.vehicle_id = vehicle_id
        self.license_plate = license_plate
        self.info = info

    def __str__(self) -> str:
        return f"Id: {self.vehicle_id}. License plate: {self.license_plate}. Info: {self.info}."


class VehicleRegistry:
    """Class representing a basic vehicle registration system."""

    def __init__(self) -> None:
        self.vehicle_info: list[VehicleInfo] = [
            VehicleInfo("Tesla", "Model 3", 50000),
            VehicleInfo("Volkswagen", "ID3", 35000),
            VehicleInfo("BMW", "520e", 60000, False),
            VehicleInfo("Tesla", "Model Y", 55000),
        ]
        self.online = True

    def find_vehicle_info(self, brand: str, model: str) -> Optional[VehicleInfo]:
        """Finds vehicle info for a brand and model. If no info can be found, None is returned."""
        for vehicle_info in self.vehicle_info:
            if vehicle_info.brand != brand or vehicle_info.model != model:
                continue
            return vehicle_info
        return None

    @staticmethod
    def generate_vehicle_id(length: int) -> str:
        """Helper method for generating a random vehicle id."""
        return "".join(random.choices(string.ascii_uppercase, k=length))

    @staticmethod
    def generate_vehicle_license(vehicle_id: str) -> str:
        """Helper method for generating a vehicle license number."""

        digit_part = "".join(random.choices(string.digits, k=2))
        letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{vehicle_id[:2]}-{digit_part}-{letter_part}"

    def create_vehicle(self, brand: str, model: str) -> Vehicle:
        """Creates a new vehicle and generates an id and a license plate."""
        vehicle_info = self.find_vehicle_info(brand, model)
        if not vehicle_info:
            raise VehicleInfoMissingError(brand, model)

        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, vehicle_info)

    def online_status(self) -> RegistryStatus:
        """Reports whether the registry system is online."""
        if not self.online:
            return RegistryStatus.OFFLINE
        return (
            RegistryStatus.CONNECTION_ERROR
            if len(self.vehicle_info) == 0
            else RegistryStatus.ONLINE
        )


def main() -> None:
    """Main function."""

    # create a registry instance
    registry = VehicleRegistry()

    # verify that the registry is online
    print(f"Registry status: {registry.online_status()}")

    vehicle = registry.create_vehicle("Volkswagen", "ID3")

    # print out the vehicle information
    print(vehicle)


if __name__ == "__main__":
    main()
