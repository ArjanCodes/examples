from weather import WeatherService
from unittest.mock import patch, MagicMock

# Section 4: Mocking with patch + MagicMock
def test_get_temperature_with_mocking():
    """
    Example of mocking httpx.get with a MagicMock.
    """
    # Create a MagicMock response object
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"current": {"temp_c": 25}}

    # Patch httpx.get so it returns our mock_response
    with patch("weather.httpx.get", return_value=mock_response) as mock_get:
        service = WeatherService(api_key="fake-key")
        temp = service.get_temperature("Paris")

        assert temp == 25
        mock_get.assert_called_once()


# Section 5: Monkey patching with monkeypatch fixture
def test_get_temperature_with_monkeypatch(monkeypatch):
    """
    Example of monkeypatching httpx.get with a manual stub.
    """

    def fake_get(url, params):
        class FakeResponse:
            def raise_for_status(self): pass
            def json(self): return {"current": {"temp_c": 19}}
        return FakeResponse()

    # Monkeypatch httpx.get to use fake_get
    monkeypatch.setattr("weather.httpx.get", fake_get)

    service = WeatherService(api_key="fake-key")
    temp = service.get_temperature("Berlin")

    assert temp == 19