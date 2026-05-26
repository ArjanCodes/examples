from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt


@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float

    def distance_to(self, other: Coordinates) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass(frozen=True)
class GeoFence:
    name: str


@dataclass
class Route:
    start: Coordinates | None = None
    destination: Coordinates | None = None
    avoid_zones: list[GeoFence] = field(default_factory=list[GeoFence])

    def avoid(self, zone: GeoFence) -> None:
        self.avoid_zones.append(zone)


@dataclass
class DroneTelemetry:
    drone_id: str
    location: Coordinates | None
    battery_level: int | None
    max_wind_speed: int | None


@dataclass
class Delivery:
    destination: Coordinates
    required_battery: int
    avoid_zones: list[GeoFence] | None = None


@dataclass
class WeatherReport:
    wind_speed: int | None


class RouteDiagnostics:
    def record(self, message: str) -> None:
        print(f"[diagnostics] {message}")


def estimate_battery_usage(start: Coordinates, destination: Coordinates) -> int:
    return round(start.distance_to(destination) * 10)


def assign_delivery(
    telemetry: DroneTelemetry,
    delivery: Delivery,
    weather: WeatherReport,
    diagnostics: RouteDiagnostics | None = None,
) -> Route | None:
    if diagnostics is not None:
        diagnostics.record("Starting route assignment")

    route = Route()

    if telemetry.location is not None:
        route.start = telemetry.location
    else:
        if diagnostics is not None:
            diagnostics.record("No GPS location available")
        return None

    if weather.wind_speed is not None:
        if telemetry.max_wind_speed is not None:
            if weather.wind_speed > telemetry.max_wind_speed:
                if diagnostics is not None:
                    diagnostics.record("Too windy for this drone")
                return None
        else:
            if diagnostics is not None:
                diagnostics.record("No wind safety rating available")
            return None
    else:
        if diagnostics is not None:
            diagnostics.record("No weather data available")
        return None

    if delivery.avoid_zones is not None:
        for zone in delivery.avoid_zones:
            route.avoid(zone)

    if telemetry.battery_level is not None:
        estimated_usage = estimate_battery_usage(
            telemetry.location,
            delivery.destination,
        )

        if telemetry.battery_level < estimated_usage:
            if diagnostics is not None:
                diagnostics.record("Battery too low")
            return None
    else:
        if diagnostics is not None:
            diagnostics.record("No battery reading available")
        return None

    route.destination = delivery.destination

    if diagnostics is not None:
        diagnostics.record("Route assigned")

    return route


def main() -> None:
    telemetry = DroneTelemetry(
        drone_id="drone-1",
        location=Coordinates(0, 0),
        battery_level=80,
        max_wind_speed=35,
    )

    delivery = Delivery(
        destination=Coordinates(3, 4),
        required_battery=50,
        avoid_zones=[GeoFence("city-center")],
    )

    weather = WeatherReport(wind_speed=20)
    diagnostics = RouteDiagnostics()

    route = assign_delivery(telemetry, delivery, weather, diagnostics)

    if route is None:
        print("No route could be assigned.")
    else:
        print(route)


if __name__ == "__main__":
    main()
