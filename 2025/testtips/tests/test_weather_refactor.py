from weather_refactor import WeatherService

def test_get_temperature_with_stub_client():
    class StubClient:
        def get(self, url, params):
            class Response:
                def raise_for_status(self): pass
                def json(self): return {"current": {"temp_c": 18}}
            return Response()

    service = WeatherService(client=StubClient(), api_key="fake_key")
    assert service.get_temperature("Oslo") == 18