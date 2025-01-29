from typing import Protocol


class Vehicle(Protocol):
    speed: int

    def drive(self) -> None: ...


class Car:
    def __init__(self, speed: int):
        self.speed = speed

    def drive(self) -> None:
        print(f"Driving at {self.speed} km/h")


def start_trip(vehicle: Vehicle):
    print(f"Starting trip at {vehicle.speed} km/h")
    vehicle.drive()


my_car = Car(120)
start_trip(
    my_car
)  # ✅ Works fine, even though Car didn't explicitly declare it implements Vehicle
