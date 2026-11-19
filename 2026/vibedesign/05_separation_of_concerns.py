"""Separation of concerns: calculation, storage and notification change separately.

Run: python 05_separation_of_concerns.py [--test]. Real SQLite, recorded messages.
"""

import sqlite3
import sys
import unittest
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    hour: int
    cents_per_kwh: int


@dataclass(frozen=True)
class Plan:
    plan_id: str
    hour: int
    energy_kwh: int
    cost_cents: int


# BEFORE: the dashboard calls this to preview a plan. Surprise: it also commits it.
def optimize_home(
    plan_id: str,
    rates: tuple[Rate, ...],
    energy_kwh: int,
    connection: sqlite3.Connection,
    send: Callable[[str], None],
) -> Plan:
    cheapest = min(rates, key=lambda rate: rate.cents_per_kwh)
    plan = Plan(plan_id, cheapest.hour, energy_kwh, cheapest.cents_per_kwh * energy_kwh)
    with connection:
        connection.execute(
            "INSERT INTO plans VALUES (?, ?, ?, ?)",
            (plan.plan_id, plan.hour, plan.energy_kwh, plan.cost_cents),
        )
    send(f"Charging at {plan.hour:02}:00: {plan.energy_kwh} kWh")
    return plan


# AFTER: preview is just a calculation; applying is an explicit workflow.
def calculate_plan(plan_id: str, rates: tuple[Rate, ...], energy_kwh: int) -> Plan:
    if not plan_id.strip() or not rates or energy_kwh <= 0:
        raise ValueError("Supply a plan ID, prices and positive charging energy")
    if len({rate.hour for rate in rates}) != len(rates):
        raise ValueError("Price hours must be unique")
    cheapest = min(rates, key=lambda rate: (rate.cents_per_kwh, rate.hour))
    return Plan(plan_id, cheapest.hour, energy_kwh, cheapest.cents_per_kwh * energy_kwh)


@dataclass
class PlanRepository:
    connection: sqlite3.Connection

    def save(self, plan: Plan) -> None:
        # One row per user-confirmed plan, including when storage is retried.
        with self.connection:
            self.connection.execute(
                "INSERT INTO plans VALUES (?, ?, ?, ?) "
                "ON CONFLICT(plan_id) DO UPDATE SET hour=excluded.hour, "
                "energy_kwh=excluded.energy_kwh, cost_cents=excluded.cost_cents",
                (plan.plan_id, plan.hour, plan.energy_kwh, plan.cost_cents),
            )


def notification_text(plan: Plan) -> str:
    return (
        f"Charging at {plan.hour:02}:00: {plan.energy_kwh} kWh; "
        f"estimated cost EUR {plan.cost_cents / 100:.2f}"
    )


def apply_plan(
    plan: Plan, repository: PlanRepository, send: Callable[[str], None]
) -> None:
    repository.save(plan)
    # Delivery errors propagate. Saving and sending are NOT an atomic transaction.
    send(notification_text(plan))


def create_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE plans (plan_id TEXT PRIMARY KEY, hour INTEGER NOT NULL, "
        "energy_kwh INTEGER NOT NULL, cost_cents INTEGER NOT NULL)"
    )
    return connection


def row_count(connection: sqlite3.Connection) -> int:
    return connection.execute("SELECT COUNT(*) FROM plans").fetchone()[0]


RATES = (Rate(1, 32), Rate(2, 12), Rate(3, 24))


def demo() -> None:
    connection = create_database()
    messages: list[str] = []
    try:
        optimize_home("bad-preview", RATES, 6, connection, messages.append)
        print(
            f"BEFORE: just previewing saved {row_count(connection)} plan and sent {len(messages)} message"
        )
        connection.execute("DELETE FROM plans")
        connection.commit()
        messages.clear()
        preview = calculate_plan("tonight", RATES, 6)
        print(
            f"AFTER preview: {preview}; saved={row_count(connection)}, sent={len(messages)}"
        )
        apply_plan(preview, PlanRepository(connection), messages.append)
        print(
            f"AFTER explicit apply: saved={row_count(connection)}, sent={len(messages)}"
        )
        print(messages[0])
    finally:
        connection.close()


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = create_database()
        self.addCleanup(self.connection.close)
        self.messages: list[str] = []

    def test_before_preview_has_side_effects(self) -> None:
        optimize_home("preview", RATES, 6, self.connection, self.messages.append)
        self.assertEqual(row_count(self.connection), 1)
        self.assertEqual(len(self.messages), 1)

    def test_preview_then_explicit_apply(self) -> None:
        plan = calculate_plan("tonight", RATES, 6)
        self.assertEqual(plan, Plan("tonight", 2, 6, 72))
        self.assertEqual(row_count(self.connection), 0)
        self.assertEqual(self.messages, [])
        apply_plan(plan, PlanRepository(self.connection), self.messages.append)
        self.assertEqual(row_count(self.connection), 1)
        self.assertEqual(self.messages, [notification_text(plan)])
        stored = self.connection.execute(
            "SELECT hour, energy_kwh, cost_cents FROM plans"
        ).fetchone()
        self.assertEqual(stored, (2, 6, 72))

    def test_delivery_failure_does_not_undo_saved_plan(self) -> None:
        plan = calculate_plan("tonight", RATES, 6)
        repository = PlanRepository(self.connection)

        def offline(message: str) -> None:
            raise ConnectionError("Notification service unavailable")

        with self.assertRaises(ConnectionError):
            apply_plan(plan, repository, offline)
        self.assertEqual(row_count(self.connection), 1)
        # Retry notification independently, without recalculating or rewriting.
        self.messages.append(notification_text(plan))
        repository.save(plan)
        self.assertEqual(row_count(self.connection), 1)
        self.assertEqual(len(self.messages), 1)

    def test_reject_incomplete_requests(self) -> None:
        for plan_id, rates, energy in (("", RATES, 6), ("x", (), 6), ("x", RATES, 0)):
            with self.assertRaises(ValueError):
                calculate_plan(plan_id, rates, energy)


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demo()
