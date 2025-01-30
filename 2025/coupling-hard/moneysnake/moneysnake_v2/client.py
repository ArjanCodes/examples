from typing import Any

import httpx

MB_URL = "https://moneybird.com/api"
MB_VERSION_ID = "v2"

# Moneybird settings
admin_id_ = 0
token_ = ""
timeout_ = 20


class MoneybirdClient:
    admin_id: int
    token: str
    timeout: int

    def __init__(self, admin_id: int, token: str, timeout: int = 20) -> None:
        self.admin_id = admin_id
        self.token = token
        self.timeout = timeout

    def make_request(
        self, path: str, data: dict[str, Any] | None = None, method: str = "post"
    ) -> Any:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        fullpath = f"{MB_URL}/{MB_VERSION_ID}/{self.admin_id}/{path}"

        response = httpx.request(
            method, fullpath, json=data, headers=headers, timeout=self.timeout
        )

        response.raise_for_status()

        # return json if there is content
        return response.json() if response.content else {}

    def http_get(self, path: str) -> Any:
        return self.make_request(path, method="get")

    def http_post(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return self.make_request(path, method="post", data=data)

    def http_patch(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return self.make_request(path, method="patch", data=data)

    def http_delete(self, path: str) -> Any:
        return self.make_request(path, method="delete")
