import os
from typing import Any

import requests

JSONDict = dict[str, Any]
JSONList = list[Any]
JSON = JSONDict | JSONList

MB_URL = "https://moneybird.com/api/v2"
MB_REQUEST_TIMEOUT = 20


def get_custom_field_value(obj: JSONDict, field_id: int) -> str | None:
    for field in obj["custom_fields"]:
        if field["id"] == str(field_id):
            return field["value"]
    return None


def post_moneybird_request(
    path: str, data: dict[str, Any] | None = None, method: str = "post"
) -> JSONDict:
    md_admin_id = os.getenv("MB_ADMIN_ID")
    mb_token = os.getenv("MB_TOKEN")
    headers = {
        "Authorization": f"Bearer {mb_token}",
        "Content-Type": "application/json",
    }
    fullpath = f"{MB_URL}/{md_admin_id}/{path}"
    response = requests.request(
        method, fullpath, json=data, headers=headers, timeout=MB_REQUEST_TIMEOUT
    )
    if response.status_code >= 400:
        raise requests.exceptions.HTTPError(
            f"Error: {response.status_code} {response.text}"
        )
    if (
        "application/json" not in response.headers.get("Content-Type", "")
        or not response.text
    ):
        raise requests.exceptions.HTTPError(
            f"Error: {response.status_code} {response.text}"
        )
    return response.json()
