import math


def calculate_rectangle_area(width: float, height: float) -> float:
    if width <= 0 or height <= 0:
        raise ValueError("Invalid dimensions: width and height must be greater than 0.")
    return width * height


def calculate_circle_area(radius: float) -> float:
    if radius <= 0:
        raise ValueError("Invalid radius: must be greater than 0.")
    return math.pi * radius * radius


def calculate_square_area(side_length: float) -> float:
    if side_length <= 0:
        raise ValueError("Invalid side length: must be greater than 0.")
    return side_length * side_length


def calculate_cuboid_volume(length: float, width: float, height: float) -> float:
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError(
            "Invalid dimensions: length, width, and height must be greater than 0."
        )
    return length * width * height


def calculate_cylinder_volume(radius: float, height: float) -> float:
    if radius <= 0 or height <= 0:
        raise ValueError(
            "Invalid dimensions: radius and height must be greater than 0."
        )
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
