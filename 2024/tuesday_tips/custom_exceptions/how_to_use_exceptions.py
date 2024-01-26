class CarNotAvailableException(Exception):
    pass


def rent_car(car_type: str, days: int) -> int:
    available_cars = ["sedan", "SUV", "hatchback"]
    if car_type not in available_cars:
        raise CarNotAvailableException(f"{car_type} is not available.")

    # Calculate rental cost, etc.
    rental_cost = days * 40  # Assume a fixed rate per day
    return rental_cost


def main() -> None:
    try:
        rent_car("SUB", 5)
        print("Car rented successfully.")
    except CarNotAvailableException as e:
        print(e)
        print("Please choose a different car type.")
    finally:
        print("Thank you for using our car rental service.")


if __name__ == "__main__":
    main()
