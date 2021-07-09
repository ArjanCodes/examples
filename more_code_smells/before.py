import random
import string
from dataclasses import dataclass


@dataclass
class VehicleInfo:

    brand: str
    electric: bool
    catalogue_price: int
    production_year: int

    def compute_tax(self):
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * self.catalogue_price

    def print(self):
        print(f"Brand: {self.brand}")
        print(f"Payable tax: {self.compute_tax()}")


class Vehicle:
    def __init__(self, id: str, license_plate: str, info: VehicleInfo):
        self.id = id
        self.license_plate = license_plate
        self.info = info

    def print(self):
        print(f"Id: {self.id}")
        print(f"License plate: {self.license_plate}")
        self.info.print()


class VehicleRegistry:
    def __init__(self):
        self.vehicle_info: dict[str, VehicleInfo] = {}
        self.add_vehicle_info("Tesla Model 3", True, 60000)
        self.add_vehicle_info("Volkswagen ID3", True, 35000)
        self.add_vehicle_info("BMW 5", False, 45000)
        self.add_vehicle_info("Tesla Model Y", True, 75000)

    def add_vehicle_info(self, brand: str, electric: bool, catalogue_price: int):
        self.vehicle_info[brand] = VehicleInfo(brand, electric, catalogue_price, 2021)

    def generate_vehicle_id(self, length: int):
        return "".join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id: str):
        return f"{id[:2]}-{''.join(random.choices(string.digits, k=2))}-{''.join(random.choices(string.ascii_uppercase, k=2))}"

    def create_vehicle(self, brand: str):
        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, self.vehicle_info[brand])


class Application:
    def register_vehicle(self, brand: str):
        # create a registry instance
        registry = VehicleRegistry()

        vehicle = registry.create_vehicle(brand)

        # print out the vehicle information
        vehicle.print()


app = Application()
app.register_vehicle("Volkswagen ID3")
