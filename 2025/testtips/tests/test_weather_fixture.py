import pytest
from weather import WeatherService


# This fixture creates a WeatherService instance you can reuse
@pytest.fixture
def weather_service():
    return WeatherService(api_key="fake-key")


def test_get_temperature_returns_expected_value(weather_service, monkeypatch):
    """
    Test that get_temperature returns the correct temperature.
    """

    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": 20}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    temp = weather_service.get_temperature("Amsterdam")
    assert temp == 20


def test_get_temperature_returns_float(weather_service, monkeypatch):
    """
    Test that get_temperature returns a float value.
    """

    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": 18.5}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    temp = weather_service.get_temperature("Berlin")
    assert isinstance(temp, float)
