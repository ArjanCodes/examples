import math


def validate_dimensions(*dimensions: float) -> None:
    for dimension in dimensions:
        if dimension <= 0:
            raise ValueError("Dimensions must be greater than 0.")


def calculate_rectangle_area(width: float, height: float) -> float:
    validate_dimensions(width, height)
    return width * height


def calculate_circle_area(radius: float) -> float:
    validate_dimensions(radius)
    return math.pi * radius * radius


def calculate_square_area(side_length: float) -> float:
    validate_dimensions(side_length)
    return side_length * side_length


def calculate_cuboid_volume(length: float, width: float, height: float) -> float:
    validate_dimensions(length, width, height)
    return length * width * height


def calculate_cylinder_volume(radius: float, height: float) -> float:
    validate_dimensions(radius, height)
    return math.pi * radius * radius * height


def main() -> None:
    try:
        print(f"Square area: {calculate_square_area(5)}")  # 25
        print(f"Rectangle area: {calculate_rectangle_area(4, 5)}")  # 20
        print(f"Circle area: {calculate_circle_area(3)}")  # 28.27331
        print(f"Cuboid volume: {calculate_cuboid_volume(3, 4, 5)}")  # 60
        print(f"Cylinder volume: {calculate_cylinder_volume(3, 5)}")  # 141.37167

        # This will raise an error
        print(f"Invalid cuboid volume: {calculate_cuboid_volume(-3, 4, 5)}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
