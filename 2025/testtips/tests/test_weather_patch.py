from weather import WeatherService
import pytest
from typing import Any

def test_get_temperature_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, params: dict[str, Any]) -> Any:
        class FakeResponse:
            def raise_for_status(self) -> None: pass
            def json(self) -> dict[str, Any]:
                return {"current": {"temp_c": 19}}
        return FakeResponse()

    monkeypatch.setattr("httpx.get", fake_get)
    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Amsterdam")
    assert temp == 19