"""
Basic example of a Vehicle registration system.
"""
import random
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * self.catalogue_price

    def __str__(self) -> str:
        """Returns a string representation of this instance."""
        tax = self.compute_tax()
        return f"brand: {self.brand} - type: {self.model} - tax: {tax}"


class Vehicle:
    """Class representing a vehicle (electric or fossil fuel)."""

    def __init__(self, _id: str, license_plate: str, info: VehicleInfo) -> None:
        self._id = _id
        self.license_plate = license_plate
        self.info = info

    def __str__(self) -> str:
        """Returns a string representation of this instance."""
        return (
            f"Id: {self._id}. License plate: {self.license_plate}. Info: {self.info}."
        )


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
            if vehicle_info.brand == brand and vehicle_info.model == model:
                return vehicle_info
        return None

    @staticmethod
    def generate_vehicle_id(length: int) -> str:
        """Helper method for generating a random vehicle id."""
        return "".join(random.choices(string.ascii_uppercase, k=length))

    @staticmethod
    def generate_vehicle_license(_id: str) -> str:
        """Helper method for generating a vehicle license number."""

        digit_part = "".join(random.choices(string.digits, k=2))
        letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{_id[:2]}-{digit_part}-{letter_part}"

    def create_vehicle(self, brand: str, model: str) -> Vehicle:
        """Creates a new vehicle and generates an id and a license plate."""
        vehicle_info = self.find_vehicle_info(brand, model)
        if vehicle_info is None:
            raise VehicleInfoMissingError(brand, model)

        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, vehicle_info)

    def online_status(self) -> str:
        """Reports whether the registry system is online."""
        if not self.online:
            return "Offline"
        return "Connection error" if len(self.vehicle_info) == 0 else "Online"


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
