from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    x: float
    y: float


@dataclass
class FlexiblePoint:
    x: float
    y: float


def main() -> None:
    point = Point(1.0, 2.0)
    try:
        point.label = "origin-ish"  # type: ignore[attr-defined]
    except AttributeError as error:
        print(f"Slots reject runtime extensions: {error}")

    flexible_point = FlexiblePoint(1.0, 2.0)
    flexible_point.label = "origin-ish"
    print(f"Regular dataclass extension: {flexible_point.label}")


if __name__ == "__main__":
    main()
