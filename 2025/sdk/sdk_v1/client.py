import httpx


class APIHttpClient:
    def __init__(self, token: str, base_url: str = "http://localhost:8000"):
        self.client = httpx.Client(
            base_url=base_url, headers={"Authorization": f"Bearer {token}"}
        )

    def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        response = self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: dict = None) -> httpx.Response:
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict = None) -> httpx.Response:
        return self.request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict = None) -> httpx.Response:
        return self.request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> httpx.Response:
        return self.request("DELETE", endpoint)
