import pytest
from weather import WeatherService
from typing import Any
from unittest.mock import MagicMock

@pytest.fixture
def weather_service(monkeypatch: pytest.MonkeyPatch) -> WeatherService:
    def fake_get(url: str, params: dict[str, Any]) -> Any:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"current": {"temp_c": 25}}
        return mock_response

    monkeypatch.setattr("httpx.get", fake_get)
    return WeatherService(api_key="fake-key")

def test_fixture_usage(weather_service: WeatherService) -> None:
    assert weather_service.get_temperature("Paris") == 25

