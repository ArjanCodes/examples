"""
Basic example of a Vehicle registration system.
"""
import random
import string
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Tuple


class FuelType(Enum):
    """Types of fuel used in a vehicle."""

    ELECTRIC = auto()
    PETROL = auto()


class RegistryStatus(Enum):
    """Possible statuses for the vehicle registry system."""

    ONLINE = auto()
    CONNECTION_ERROR = auto()
    OFFLINE = auto()


taxes = {FuelType.ELECTRIC: 0.02, FuelType.PETROL: 0.05}


@dataclass
class VehicleInfoMissingError(Exception):
    """Custom error that is raised when vehicle information is missing for a particular brand."""

    brand: str
    model: str
    message: str = "Vehicle information is missing."


@dataclass
class VehicleModelInfo:
    """Class that contains basic information about a vehicle model."""

    brand: str
    model: str
    catalogue_price: int
    fuel_type: FuelType = FuelType.ELECTRIC
    production_year: int = datetime.now().year

    @property
    def tax(self) -> float:
        """Tax to be paid when registering a vehicle of this type."""
        tax_percentage = taxes[self.fuel_type]
        return tax_percentage * self.catalogue_price

    def __str__(self) -> str:
        return f"brand: {self.brand} - type: {self.model} - tax: {self.tax}"


@dataclass
class Vehicle:
    """Class representing a vehicle (electric or fossil fuel)."""

    vehicle_id: str
    license_plate: str
    info: VehicleModelInfo

    def __str__(self) -> str:
        return f"Id: {self.vehicle_id}. License plate: {self.license_plate}. Info: {self.info}."


class VehicleRegistry:
    """Class representing a basic vehicle registration system."""

    def __init__(self) -> None:
        self.vehicle_models: dict[Tuple[str, str], VehicleModelInfo] = {}
        self.online = True

    def add_model_info(self, model_info: VehicleModelInfo) -> None:
        """Helper method for adding a VehicleModelInfo object to a list."""
        self.vehicle_models[(model_info.brand, model_info.model)] = model_info

    def find_model_info(self, brand: str, model: str) -> Optional[VehicleModelInfo]:
        """Finds vehicle model info for a brand and model. If no info can be found, None is returned."""
        return self.vehicle_models.get((brand, model))

    # Below is the function used before changing self.vehicle_models to a dictionary
    # def find_model_info(self, brand: str, model: str) -> Optional[VehicleModelInfo]:
    #     """Finds vehicle info for a brand and model. If no info can be found, None is returned."""
    #     for vehicle_model in self.vehicle_models:
    #         if vehicle_model.brand != brand or vehicle_model.model != model:
    #             continue
    #         return vehicle_model
    #     return None

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

    def register_vehicle(self, brand: str, model: str) -> Vehicle:
        """Register a new vehicle and generates an id and a license plate."""

        # without the walrus operator
        # vehicle_model = self.find_model_info(brand, model)
        # if not vehicle_model:
        #     raise VehicleInfoMissingError(brand, model)

        # with the walrus operator
        if not (vehicle_model := self.find_model_info(brand, model)):
            raise VehicleInfoMissingError(brand, model)

        # generate the vehicle id and license plate
        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, vehicle_model)

    def online_status(self) -> RegistryStatus:
        """Report whether the registry system is online."""
        if not self.online:
            return RegistryStatus.OFFLINE
        return (
            RegistryStatus.CONNECTION_ERROR
            if len(self.vehicle_models) == 0
            else RegistryStatus.ONLINE
        )


def main() -> None:
    """Main function."""

    # create a registry instance
    registry = VehicleRegistry()

    # add a couple of different vehicle models
    registry.add_model_info(VehicleModelInfo("Tesla", "Model 3", 50000))
    registry.add_model_info(VehicleModelInfo("Volkswagen", "ID3", 35000))
    registry.add_model_info(VehicleModelInfo("BMW", "520e", 60000, FuelType.PETROL))
    registry.add_model_info(VehicleModelInfo("Tesla", "Model Y", 55000))

    # verify that the registry is online
    print(f"Registry status: {registry.online_status()}")

    vehicle = registry.register_vehicle("Volkswagen", "ID3")

    # print out the vehicle information
    print(vehicle)


if __name__ == "__main__":
    main()
