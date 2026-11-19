"""Encapsulation: the battery owns its reserve and capacity rules.

Run: python 04_encapsulation.py [--test]. Energy uses integer watt-hours.
"""

import sys
import unittest
from dataclasses import FrozenInstanceError, dataclass


# BEFORE: each caller must remember all of the battery's invariants.
@dataclass
class ExposedBattery:
    capacity_wh: int
    reserve_wh: int
    stored_wh: int


def sell_at_peak_price(battery: ExposedBattery, requested_wh: int) -> None:
    # Checks there is enough energy, but forgets the backup reserve.
    if requested_wh > battery.stored_wh:
        raise ValueError("Not enough energy")
    battery.stored_wh -= requested_wh


@dataclass(frozen=True)
class BatterySnapshot:
    capacity_wh: int
    reserve_wh: int
    stored_wh: int


def require_wh(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError("Energy must be a nonnegative integer number of Wh")


# AFTER: every public state transition preserves reserve <= stored <= capacity.
class Battery:
    def __init__(self, capacity_wh: int, reserve_wh: int, stored_wh: int) -> None:
        for amount in (capacity_wh, reserve_wh, stored_wh):
            require_wh(amount)
        if capacity_wh == 0 or not reserve_wh <= stored_wh <= capacity_wh:
            raise ValueError("Require 0 <= reserve <= stored <= positive capacity")
        self._capacity_wh = capacity_wh
        self._reserve_wh = reserve_wh
        self._stored_wh = stored_wh

    @property
    def available_wh(self) -> int:
        return self._stored_wh - self._reserve_wh

    def charge(self, amount_wh: int) -> None:
        require_wh(amount_wh)
        if self._stored_wh + amount_wh > self._capacity_wh:
            raise ValueError("Charge would exceed battery capacity")
        self._stored_wh += amount_wh

    def discharge(self, amount_wh: int) -> None:
        require_wh(amount_wh)
        if amount_wh > self.available_wh:
            raise ValueError("Discharge would consume the backup reserve")
        self._stored_wh -= amount_wh

    def set_reserve(self, reserve_wh: int) -> None:
        require_wh(reserve_wh)
        if reserve_wh > self._stored_wh:
            raise ValueError("Reserve cannot exceed stored energy")
        self._reserve_wh = reserve_wh

    def snapshot(self) -> BatterySnapshot:
        return BatterySnapshot(self._capacity_wh, self._reserve_wh, self._stored_wh)


def demo() -> None:
    exposed = ExposedBattery(capacity_wh=10_000, reserve_wh=2_000, stored_wh=7_000)
    sell_at_peak_price(exposed, 6_000)
    print(
        f"BEFORE: {exposed.stored_wh} Wh left; promised backup reserve: {exposed.reserve_wh} Wh"
    )
    print("The backup plan now requires a candle.")
    battery = Battery(capacity_wh=10_000, reserve_wh=2_000, stored_wh=7_000)
    try:
        battery.discharge(6_000)
    except ValueError as error:
        print(f"AFTER: rejected: {error}; state unchanged: {battery.snapshot()}")
    battery.discharge(battery.available_wh)
    print("Selling only available energy preserves the reserve:", battery.snapshot())


class Tests(unittest.TestCase):
    def test_before_bypasses_reserve(self) -> None:
        battery = ExposedBattery(10_000, 2_000, 7_000)
        sell_at_peak_price(battery, 6_000)
        self.assertLess(battery.stored_wh, battery.reserve_wh)

    def test_rejected_transitions_leave_state_unchanged(self) -> None:
        battery = Battery(10_000, 2_000, 7_000)
        original = battery.snapshot()
        for operation, amount in (
            (battery.discharge, 6_000),
            (battery.charge, 3_001),
            (battery.set_reserve, 7_001),
            (battery.discharge, -1),
            (battery.charge, float("nan")),
            (battery.charge, True),
        ):
            with self.subTest(operation=operation.__name__, amount=amount):
                with self.assertRaises(ValueError):
                    operation(amount)
                self.assertEqual(battery.snapshot(), original)

    def test_boundary_transitions_and_immutable_snapshot(self) -> None:
        battery = Battery(10_000, 2_000, 7_000)
        snapshot = battery.snapshot()
        with self.assertRaises(FrozenInstanceError):
            snapshot.stored_wh = 0
        battery.discharge(5_000)
        self.assertEqual(battery.available_wh, 0)
        battery.charge(8_000)
        self.assertEqual(battery.snapshot().stored_wh, 10_000)
        battery.set_reserve(3_000)
        self.assertEqual(battery.available_wh, 7_000)
        self.assertEqual(snapshot.stored_wh, 7_000)

    def test_invalid_initial_state(self) -> None:
        for values in ((0, 0, 0), (10_000, 8_000, 7_000), (10_000, 0, 11_000)):
            with self.assertRaises(ValueError):
                Battery(*values)


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demo()
