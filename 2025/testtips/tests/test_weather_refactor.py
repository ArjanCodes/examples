from unittest.mock import MagicMock

import pytest

from weather_refactor import WeatherService


@pytest.fixture
def weather_service() -> WeatherService:
    mock_http_client = MagicMock()
    mock_http_client.get.return_value = MagicMock(
        **{
            "raise_for_status": lambda: None,
            "json": lambda: {"current": {"temp_c": 17}},
        }
    )
    return WeatherService(client=mock_http_client, api_key="fake-key")


def test_weather_service_with_mock_http_client(weather_service: WeatherService):
    temp = weather_service.get_temperature("Amsterdam")
    assert temp == 17
