import httpx

class ExchangeRateService:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_rate(self, from_currency: str, to_currency: str) -> float:
        url = f"{self.api_url}?base={from_currency}&symbols={to_currency}"
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get(to_currency)
        if not rate or rate <= 0:
            raise ValueError("Invalid exchange rate")
        return rate