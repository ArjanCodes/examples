from dataclasses import dataclass


# Define a base class named Vehicle
@dataclass
class Vehicle:
    model: str

    def display(self) -> None:
        print(f"Vehicle model: {self.model}")


# Define two subclasses for Vehicle: Car and Boat
class Car(Vehicle):
    def display(self) -> None:
        print(f"Car model: {self.model}")


class Boat(Vehicle):
    def display(self) -> None:
        print(f"Boat model: {self.model}")


class Plane(Vehicle):
    def display(self) -> None:
        print(f"Plane model: {self.model}")


class VehicleRegistry[V: Vehicle]:
    def __init__(self) -> None:
        self.vehicles: list[V] = []

    def add_vehicle(self, vehicle: V) -> None:
        self.vehicles.append(vehicle)

    def display_all(self) -> None:
        for vehicle in self.vehicles:
            vehicle.display()


def main() -> None:
    # Usage
    registry = VehicleRegistry[Car]()
    registry.add_vehicle(Car("Sedan"))
    registry.add_vehicle(Car("SUV"))
    registry.display_all()

    # This will raise a type error
    # registry.add_vehicle(Boat("Yacht"))

    # If you need a registry that accepts any kind of Vehicle (or its subclasses)
    generic_registry = VehicleRegistry[Vehicle]()
    generic_registry.add_vehicle(Car("Convertible"))
    generic_registry.add_vehicle(Boat("Cruiser"))
    generic_registry.display_all()


if __name__ == "__main__":
    main()
