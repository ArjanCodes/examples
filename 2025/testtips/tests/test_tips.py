import sys
from typing import Any

import pytest

from weather import WeatherService


@pytest.mark.parametrize(
    "city,expected_temp",
    [
        ("London", 15),
        ("Berlin", 20),
        ("Rome", 18),
    ],
)
def test_parametrized_temperatures(
    monkeypatch: pytest.MonkeyPatch, city: str, expected_temp: float
) -> None:
    def fake_get(url: str, params: dict[str, Any]) -> Any:
        class FakeResponse:
            def raise_for_status(self) -> None:
                pass

            def json(self) -> dict[str, Any]:
                return {"current": {"temp_c": expected_temp}}

        return FakeResponse()

    monkeypatch.setattr("httpx.get", fake_get)
    service = WeatherService(api_key="fake-key")
    assert service.get_temperature(city) == expected_temp


def test_temperature_raises_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, params: dict[str, Any]) -> Any:
        class FakeResponse:
            def raise_for_status(self) -> None:
                raise Exception("API error")

        return FakeResponse()

    monkeypatch.setattr("httpx.get", fake_get)
    service = WeatherService(api_key="fake-key")

    with pytest.raises(Exception):
        service.get_temperature("Oslo")


@pytest.mark.skip(reason="Temporarily skipping for demo purposes")
def test_skipped() -> None:
    assert False


@pytest.mark.skipif(sys.platform == "win32", reason="Fails on Windows")
def test_non_windows_behavior() -> None:
    assert True


@pytest.mark.xfail(reason="Intentional failure due to API bug")
def test_expected_failure() -> None:
    assert 1 + 1 == 3
