import httpx
import pytest
from weather import WeatherService


# Tip 1: Single assert per test
def test_get_temperature_returns_expected_value(monkeypatch):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": 22}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Amsterdam")

    assert temp == 22


# Tip 2: Clear and descriptive names
def test_get_temperature_for_different_city(monkeypatch):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": 18}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Berlin")

    assert temp == 18


def test_get_temperature_handles_api_error(monkeypatch):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                raise httpx.HTTPError("API error")

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")

    with pytest.raises(httpx.HTTPError):
        service.get_temperature("Paris")


def test_get_temperature_returns_float(monkeypatch):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": 19.5}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Rome")

    assert isinstance(temp, float)
