from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from weather import WeatherService


def test_get_temperature_with_mocking_monkeypatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, params: dict[str, Any]) -> Any:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"current": {"temp_c": 25}}
        return mock_response

    monkeypatch.setattr("httpx.get", fake_get)
    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Amsterdam")
    assert temp == 25


def test_get_temperature_with_mocking() -> None:
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"current": {"temp_c": 25}}

    with patch("httpx.get", return_value=mock_response) as mock_get:
        service = WeatherService(api_key="fake-key")
        temp = service.get_temperature("London")

        assert temp == 25
        mock_get.assert_called_once()
