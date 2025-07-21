# tests/test_weather.py

import sys

import pytest
from weather import WeatherService

# from hypothesis import given
# from hypothesis.strategies import floats


# ✅ Parametrization
@pytest.mark.parametrize(
    "city,expected_temp", [("London", 15), ("Berlin", 20), ("Paris", 17)]
)
def test_get_temperature_multiple_cities(monkeypatch, city, expected_temp):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"current": {"temp_c": expected_temp}}

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature(city)

    assert temp == expected_temp


# ✅ pytest.raises
def test_get_temperature_raises_http_error(monkeypatch):
    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self):
                raise Exception("API error")

        return FakeResponse()

    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")

    with pytest.raises(Exception):
        service.get_temperature("Tokyo")


# ✅ pytest.mark.skip
@pytest.mark.skip(reason="Skipping this test for demonstration purposes.")
def test_skipped_example():
    assert False


# ✅ pytest.mark.skipif
@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_only_runs_on_non_windows():
    assert True


# ✅ pytest.mark.xfail
@pytest.mark.xfail(reason="Known bug: API sometimes returns wrong temperature")
def test_expected_failure_example():
    assert 2 + 2 == 5


# ✅ Hypothesis property-based test
# @given(floats(min_value=-50, max_value=50))
# def test_temperature_range_property(temp):
#     assert -50 <= temp <= 50
