import httpx

_client = None
_token = None
_base_url = "http://localhost:8000"


def set_credentials(token: str):
    global _client, _token, _base_url
    _token = token
    _client = httpx.Client(
        base_url=_base_url, headers={"Authorization": f"Bearer {_token}"}
    )


def request(method: str, endpoint: str, **kwargs) -> httpx.Response:
    if _client is None:
        raise RuntimeError("Credentials not set. Call set_credentials() first.")
    response = _client.request(method, endpoint, **kwargs)
    response.raise_for_status()
    return response


def get(endpoint: str, params: dict = None) -> httpx.Response:
    return request("GET", endpoint, params=params)


def post(endpoint: str, json: dict = None) -> httpx.Response:
    return request("POST", endpoint, json=json)


def put(endpoint: str, json: dict = None) -> httpx.Response:
    return request("PUT", endpoint, json=json)


def delete(endpoint: str) -> httpx.Response:
    return request("DELETE", endpoint)
