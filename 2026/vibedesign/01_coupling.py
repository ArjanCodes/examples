"""Coupling: credentials and provider details should not enter scheduling logic.

Run: python 01_coupling.py [--test]. Fictional provider; demo HTTP is mocked.
"""

import json
import os
import sys
import unittest
from dataclasses import dataclass, field
from decimal import Decimal
from io import BytesIO
from unittest.mock import patch
from urllib.request import Request, urlopen


# BEFORE: even a scheduling test needs environment and HTTP setup.
def tightly_coupled_schedule(hours_needed: int) -> tuple[str, ...]:
    token = os.environ["ENERGY_API_TOKEN"]
    meter_id = os.environ["ENERGY_METER_ID"]
    api = EnergyProviderAPI(token, meter_id)
    rows = api.hourly_prices()
    if not 1 <= hours_needed <= len(rows):
        raise ValueError("Not enough hourly prices for the requested charge")
    cheapest = sorted(rows, key=lambda row: Decimal(row["import_eur_per_kwh"]))
    return tuple(sorted(row["start"] for row in cheapest[:hours_needed]))


# Provider-specific HTTP and JSON live at the boundary.
class EnergyProviderAPI:
    """Illustrative contract, not a client for a real energy supplier."""

    def __init__(self, token: str, meter_id: str) -> None:
        self._token = token
        self._meter_id = meter_id

    def hourly_prices(self) -> list[dict[str, str]]:
        request = Request(
            "https://api.energy-provider.example/v1/hourly-prices",
            headers={
                "Authorization": f"Bearer {self._token}",
                "X-Meter-ID": self._meter_id,
                "Accept": "application/json",
            },
        )
        with urlopen(request, timeout=5) as response:
            payload = json.load(response)
        return payload["prices"]


# AFTER: configuration, provider adapter, domain function, composition.
@dataclass(frozen=True)
class Settings:
    token: str = field(repr=False)
    meter_id: str

    @classmethod
    def from_environment(cls) -> "Settings":
        token = os.environ.get("ENERGY_API_TOKEN", "").strip()
        meter_id = os.environ.get("ENERGY_METER_ID", "").strip()
        if not token or not meter_id:
            raise ValueError("Set ENERGY_API_TOKEN and ENERGY_METER_ID")
        return cls(token, meter_id)


@dataclass(frozen=True)
class PriceSlot:
    # Contract: unique, consecutive one-hour UTC slots, chronological ISO labels.
    start: str
    eur_per_kwh: Decimal

    def __post_init__(self) -> None:
        if not self.eur_per_kwh.is_finite():
            raise ValueError("Price must be finite; negative prices are allowed")


def fetch_prices(api: EnergyProviderAPI) -> tuple[PriceSlot, ...]:
    return tuple(
        PriceSlot(row["start"], Decimal(row["import_eur_per_kwh"]))
        for row in api.hourly_prices()
    )


def cheapest_hours(prices: tuple[PriceSlot, ...], hours_needed: int) -> tuple[str, ...]:
    """Fixed-power EV charging may pause between slots; deadline is the horizon end."""
    if not 1 <= hours_needed <= len(prices):
        raise ValueError("Not enough hourly prices for the requested charge")
    if len({slot.start for slot in prices}) != len(prices):
        raise ValueError("Duplicate price slots")
    selected = sorted(prices, key=lambda slot: (slot.eur_per_kwh, slot.start))
    return tuple(sorted(slot.start for slot in selected[:hours_needed]))


def configured_schedule(hours_needed: int) -> tuple[str, ...]:
    settings = Settings.from_environment()
    api = EnergyProviderAPI(settings.token, settings.meter_id)
    return cheapest_hours(fetch_prices(api), hours_needed)


FIXTURE = {
    "prices": [
        {"start": "2026-11-03T01:00:00Z", "import_eur_per_kwh": "0.32"},
        {"start": "2026-11-03T02:00:00Z", "import_eur_per_kwh": "-0.02"},
        {"start": "2026-11-03T03:00:00Z", "import_eur_per_kwh": "0.12"},
    ]
}


def fake_http(request: Request, timeout: int) -> BytesIO:
    return BytesIO(json.dumps(FIXTURE).encode())


def demo() -> None:
    with patch.dict(os.environ, {}, clear=True):
        try:
            tightly_coupled_schedule(2)
        except KeyError as error:
            print(f"BEFORE: cannot calculate a schedule without {error}")
        prices = tuple(
            PriceSlot(row["start"], Decimal(row["import_eur_per_kwh"]))
            for row in FIXTURE["prices"]
        )
        print("AFTER: offline domain calculation:", cheapest_hours(prices, 2))
    with (
        patch.dict(
            os.environ, ENERGY_API_TOKEN="demo-token", ENERGY_METER_ID="meter-42"
        ),
        patch(__name__ + ".urlopen", side_effect=fake_http),
    ):
        print("Same result through configured API adapter:", configured_schedule(2))


class Tests(unittest.TestCase):
    def test_http_credentials_mapping_and_behavior_preserved(self) -> None:
        with (
            patch.dict(
                os.environ, ENERGY_API_TOKEN="demo-token", ENERGY_METER_ID="meter-42"
            ),
            patch(__name__ + ".urlopen", side_effect=fake_http) as http,
        ):
            before = tightly_coupled_schedule(2)
            after = configured_schedule(2)
        self.assertEqual(before, after)
        self.assertEqual(after, ("2026-11-03T02:00:00Z", "2026-11-03T03:00:00Z"))
        request = http.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer demo-token")
        self.assertEqual(request.get_header("X-meter-id"), "meter-42")
        self.assertEqual(http.call_args.kwargs["timeout"], 5)

    def test_domain_needs_neither_environment_nor_http(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            patch(__name__ + ".urlopen", side_effect=AssertionError("Unexpected HTTP")),
        ):
            slots = (
                PriceSlot("01:00", Decimal("0.2")),
                PriceSlot("02:00", Decimal("-0.1")),
            )
            self.assertEqual(cheapest_hours(slots, 1), ("02:00",))
            with self.assertRaises(ValueError):
                cheapest_hours(slots, 3)

    def test_missing_config_fails_without_exposing_credentials(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                Settings.from_environment()
        self.assertNotIn("secret", repr(Settings("secret", "meter-42")))


if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demo()
