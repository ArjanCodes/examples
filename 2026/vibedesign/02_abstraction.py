"""Abstraction: ask for energy, rather than teaching the optimizer every device API.

Run: python 02_abstraction.py [--test]. SDK stand-ins only record commands.
"""

import math
import sys
import unittest
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class WallboxSDK:
    commands: list[tuple[int, int]] = field(default_factory=list[tuple[int, int]])

    def start_session(self, *, watts: int, seconds: int) -> None:
        self.commands.append((watts, seconds))


@dataclass
class HeaterSDK:
    commands: list[tuple[float, int]] = field(default_factory=list[tuple[float, int]])

    def boost(self, *, kilowatts: float, minutes: int) -> None:
        self.commands.append((kilowatts, minutes))


# BEFORE: every new device changes this function, with different units per branch.
def optimize_device(device: WallboxSDK | HeaterSDK, surplus_kwh: float) -> None:
    if isinstance(device, WallboxSDK):
        device.start_session(watts=3000, seconds=round(surplus_kwh / 3 * 3600))
    elif isinstance(device, HeaterSDK):
        # A plausible unit bug: this API takes minutes, not seconds.
        device.boost(kilowatts=3, minutes=round(surplus_kwh / 3 * 3600))
    else:
        raise TypeError("Unsupported device; edit the optimizer again")


# AFTER: one small domain capability, implemented by two actual adapters.
class FlexibleLoad(Protocol):
    def absorb(self, energy_kwh: float, available_minutes: int) -> float:
        """Request energy within a window; return the kWh actually requested."""
        ...


def duration_minutes(energy_kwh: float, power_kw: float, window: int) -> int:
    if not math.isfinite(energy_kwh) or energy_kwh < 0 or window < 0:
        raise ValueError("Energy and available time must be finite and nonnegative")
    # Round down: whole-minute commands must not exceed the energy budget.
    return min(window, math.floor(energy_kwh / power_kw * 60))


@dataclass
class EVCharger:
    api: WallboxSDK

    def absorb(self, energy_kwh: float, available_minutes: int) -> float:
        minutes = duration_minutes(energy_kwh, 3, available_minutes)
        if minutes:
            self.api.start_session(watts=3000, seconds=minutes * 60)
        return 3 * minutes / 60


@dataclass
class WaterHeater:
    api: HeaterSDK

    def absorb(self, energy_kwh: float, available_minutes: int) -> float:
        minutes = duration_minutes(energy_kwh, 3, available_minutes)
        if minutes:
            self.api.boost(kilowatts=3, minutes=minutes)
        return 3 * minutes / 60


def use_solar_surplus(
    load: FlexibleLoad, surplus_kwh: float, window_minutes: int
) -> float:
    return load.absorb(surplus_kwh, window_minutes)


def demo() -> None:
    bad_heater = HeaterSDK()
    optimize_device(bad_heater, 1.5)
    print(
        f"BEFORE: 1.5 kWh requested -> heater runs {bad_heater.commands[0][1]} minutes"
    )
    print("That's a remarkably thorough shower.")
    for load in (EVCharger(WallboxSDK()), WaterHeater(HeaterSDK())):
        requested = use_solar_surplus(load, 1.5, 60)
        print(
            f"AFTER: {type(load).__name__}: {requested:.1f} kWh; commands={load.api.commands}"
        )


class Tests(unittest.TestCase):
    def test_before_requests_sixty_times_too_much_energy(self) -> None:
        heater = HeaterSDK()
        optimize_device(heater, 1.5)
        power, minutes = heater.commands[0]
        self.assertEqual(power * minutes / 60, 90)

    def test_both_adapters_deliver_the_same_domain_request(self) -> None:
        wallbox, heater = WallboxSDK(), HeaterSDK()
        self.assertEqual(use_solar_surplus(EVCharger(wallbox), 1.5, 60), 1.5)
        self.assertEqual(use_solar_surplus(WaterHeater(heater), 1.5, 60), 1.5)
        self.assertEqual(wallbox.commands, [(3000, 1800)])
        self.assertEqual(heater.commands, [(3, 30)])

    def test_window_limit_rounding_and_no_op(self) -> None:
        for load in (EVCharger(WallboxSDK()), WaterHeater(HeaterSDK())):
            with self.subTest(load=type(load).__name__):
                self.assertEqual(load.absorb(10, 20), 1)
                commands = len(load.api.commands)
                self.assertEqual(load.absorb(0, 60), 0)
                self.assertEqual(load.absorb(0.001, 60), 0)
                self.assertEqual(len(load.api.commands), commands)
                for invalid in (-1, float("nan"), float("inf")):
                    with self.assertRaises(ValueError):
                        load.absorb(invalid, 60)

    def test_new_load_needs_no_optimizer_branch(self) -> None:
        class HomeBattery:
            def absorb(self, energy_kwh: float, available_minutes: int) -> float:
                return min(energy_kwh, available_minutes / 60 * 2)

        self.assertEqual(use_solar_surplus(HomeBattery(), 3, 60), 2)


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demo()
