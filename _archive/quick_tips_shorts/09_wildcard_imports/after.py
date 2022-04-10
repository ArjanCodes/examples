import random
import string


def generate_vehicle_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


def generate_vehicle_license(_id: str) -> str:
    id_part = _id[:2]
    number_part = "".join(random.choices(string.digits, k=2))
    letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
    return f"{id_part}-{number_part}-{letter_part}"


def main():
    vehicle_id = generate_vehicle_id()
    vehicle_license = generate_vehicle_license(vehicle_id)
    print(f"Vehicle ID: {vehicle_id}")
    print(f"Vehicle license: {vehicle_license}")


if __name__ == "__main__":
    main()
