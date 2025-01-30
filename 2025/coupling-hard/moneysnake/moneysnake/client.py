from typing import Any

import httpx

MB_URL = "https://moneybird.com/api"
MB_VERSION_ID = "v2"

# Moneybird settings
admin_id_ = 0
token_ = ""
timeout_ = 20


def set_admin_id(admin_id: int) -> None:
    global admin_id_
    admin_id_ = admin_id


def set_token(token: str) -> None:
    global token_
    token_ = token


def set_timeout(timeout: int) -> None:
    global timeout_
    timeout_ = timeout


def make_request(
    path: str, data: dict[str, Any] | None = None, method: str = "post"
) -> Any:
    headers = {
        "Authorization": f"Bearer {token_}",
        "Content-Type": "application/json",
    }
    fullpath = f"{MB_URL}/{MB_VERSION_ID}/{admin_id_}/{path}"
    response = httpx.request(
        method, fullpath, json=data, headers=headers, timeout=timeout_
    )
    response.raise_for_status()

    # return json if there is content
    return response.json() if response.content else {}


def http_get(path: str) -> Any:
    return make_request(path, method="get")


def http_post(path: str, data: dict[str, Any] | None = None) -> Any:
    return make_request(path, method="post", data=data)


def http_patch(path: str, data: dict[str, Any] | None = None) -> Any:
    return make_request(path, method="patch", data=data)


def http_delete(path: str) -> Any:
    return make_request(path, method="delete")
