"""Cohesion: keep tariff knowledge together and give consumers one snapshot.

Run: python 03_cohesion.py [--test]. Prices are integer euro cents per kWh.
"""

import sys
import unittest
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    hour: int
    cents_per_kwh: int


# BEFORE: one controller owns pricing, planning and display rules.
# Tariff knowledge is duplicated, even though these methods live together.
@dataclass
class HomeController:
    fetch_rates: Callable[[], tuple[Rate, ...]]
    grid_fee_cents: int
    target_temperature_c: float = 20

    def heating_required(self, room_temperature_c: float) -> bool:
        # Comfort policy has a completely different reason to change than tariffs.
        return room_temperature_c < self.target_temperature_c - 0.5

    def charging_hour(self) -> int:
        rates = self.fetch_rates()
        return min(
            rates, key=lambda rate: rate.cents_per_kwh + self.grid_fee_cents
        ).hour

    def estimated_cost_cents(self, hour: int, energy_kwh: int) -> int:
        rates = self.fetch_rates()  # A second request can see a revised price.
        rate = next(rate for rate in rates if rate.hour == hour)
        return (rate.cents_per_kwh + self.grid_fee_cents) * energy_kwh


# AFTER: rates and the operations that interpret them belong together.
@dataclass(frozen=True)
class ComfortPolicy:
    target_temperature_c: float = 20

    def heating_required(self, room_temperature_c: float) -> bool:
        return room_temperature_c < self.target_temperature_c - 0.5


@dataclass(frozen=True)
class TariffSnapshot:
    rates: tuple[Rate, ...]
    grid_fee_cents: int

    def __post_init__(self) -> None:
        if not self.rates or len({rate.hour for rate in self.rates}) != len(self.rates):
            raise ValueError("Supply nonempty rates with unique hours")

    def import_price(self, hour: int) -> int:
        for rate in self.rates:
            if rate.hour == hour:
                return rate.cents_per_kwh + self.grid_fee_cents
        raise ValueError(f"No price for hour {hour}")

    def cheapest_hour(self) -> int:
        return min(
            self.rates, key=lambda rate: (self.import_price(rate.hour), rate.hour)
        ).hour

    def cost_cents(self, hour: int, energy_kwh: int) -> int:
        if energy_kwh < 0:
            raise ValueError("Import energy must be nonnegative")
        return self.import_price(hour) * energy_kwh


@dataclass(frozen=True)
class ChargingPlan:
    hour: int
    energy_kwh: int


def plan_charge(tariff: TariffSnapshot, energy_kwh: int) -> ChargingPlan:
    if energy_kwh <= 0:
        raise ValueError("Requested charge must be positive")
    return ChargingPlan(tariff.cheapest_hour(), energy_kwh)


def render_estimate(plan: ChargingPlan, tariff: TariffSnapshot) -> str:
    cost = tariff.cost_cents(plan.hour, plan.energy_kwh)
    return f"Charge {plan.energy_kwh} kWh at {plan.hour:02}:00; estimate EUR {cost / 100:.2f}"


OLD_RATES = (Rate(1, 10), Rate(2, 20))
REVISED_RATES = (Rate(1, 50), Rate(2, 20))


def demo() -> None:
    updates = iter((OLD_RATES, REVISED_RATES))
    controller = HomeController(lambda: next(updates), grid_fee_cents=5)
    hour = controller.charging_hour()
    cost = controller.estimated_cost_cents(hour, 6)
    print(
        f"BEFORE: chose {hour:02}:00 using 10-cent energy; dashboard now quotes EUR {cost / 100:.2f}"
    )
    tariff = TariffSnapshot(OLD_RATES, grid_fee_cents=5)
    plan = plan_charge(tariff, 6)
    print("AFTER:", render_estimate(plan, tariff))
    print(
        "One tariff snapshot; one definition of import price. A refreshed tariff needs a refreshed plan."
    )


class Tests(unittest.TestCase):
    def test_before_dashboard_and_scheduler_use_different_prices(self) -> None:
        updates = iter((OLD_RATES, REVISED_RATES))
        home = HomeController(lambda: next(updates), 5)
        hour = home.charging_hour()
        self.assertEqual(hour, 1)
        self.assertEqual(home.estimated_cost_cents(hour, 6), 330)
        self.assertEqual(
            min(REVISED_RATES, key=lambda rate: rate.cents_per_kwh).hour, 2
        )

    def test_same_snapshot_drives_plan_and_display(self) -> None:
        tariff = TariffSnapshot(OLD_RATES, 5)
        plan = plan_charge(tariff, 6)
        self.assertEqual(plan, ChargingPlan(1, 6))
        self.assertEqual(tariff.cost_cents(plan.hour, plan.energy_kwh), 90)
        self.assertIn("EUR 0.90", render_estimate(plan, tariff))
        refreshed = TariffSnapshot(REVISED_RATES, 5)
        self.assertEqual(plan_charge(refreshed, 6).hour, 2)

    def test_fee_negative_price_and_invalid_snapshot(self) -> None:
        tariff = TariffSnapshot((Rate(1, -10), Rate(2, 0)), 5)
        self.assertEqual(tariff.cost_cents(tariff.cheapest_hour(), 6), -30)
        with self.assertRaises(ValueError):
            tariff.import_price(3)
        for rates in ((), (Rate(1, 10), Rate(1, 20))):
            with self.assertRaises(ValueError):
                TariffSnapshot(rates, 5)

    def test_comfort_policy_has_no_tariff_dependency(self) -> None:
        comfort = ComfortPolicy(target_temperature_c=21)
        self.assertTrue(comfort.heating_required(19))
        self.assertFalse(comfort.heating_required(21))


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demo()
