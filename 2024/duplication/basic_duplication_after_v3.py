import math


def validate_dimensions(*dimensions: float) -> None:
    for dimension in dimensions:
        if dimension <= 0:
            raise ValueError("Dimensions must be greater than 0.")


def calculate_any_volume(
    dimensions: list[float], square_first: bool, multiply: bool
) -> float:
    validate_dimensions(*dimensions)
    result = 1
    for i, dimension in enumerate(dimensions):
        if i == 0 and square_first:
            result = result * dimension * dimension
        else:
            result = result * dimension
    if multiply:
        result = math.pi * result
    return result


def main() -> None:
    try:
        print(f"Square area: {calculate_any_volume([5], True, False)}")  # 25
        print(f"Rectangle area: {calculate_any_volume([4, 5], False, False)}")  # 20
        print(f"Circle area: {calculate_any_volume([3], True, True)}")  # 28.27331
        print(f"Cuboid volume: {calculate_any_volume([3, 4, 5], False, False)}")  # 60
        print(
            f"Cylinder volume: {calculate_any_volume([3, 5], True, True)}"
        )  # 141.37167

        # This will raise an error
        print(
            f"Invalid cuboid volume: {calculate_any_volume([-3, 4, 5], False, False)}"
        )

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
