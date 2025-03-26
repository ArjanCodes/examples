API_URL = "https://api.company.com"
API_VERSION_ID = "v2"
TOKEN = "a3f5c7e8d9b1c2e3f4a5b62e3f4a5b6c7d8e9f0a1"
ACCOUNT_ID = 98753244984

type JSONDict = dict[str, str | int | float | bool | None]


def make_request(
    api_url: str,
    api_version: str,
    path: str,
    data: JSONDict | None,
    method: str,
    token: str,
    account_id: int,
) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    fullpath = f"{api_url}/{api_version}/{account_id}/{path}"
    print(f"Making request to {fullpath}")
    print(f"Data: {data}")
    print(f"Method: {method}")
    print(f"Headers: {headers}")


def main() -> None:
    make_request(
        API_URL, API_VERSION_ID, "invoices", {"amount": 1000}, "post", TOKEN, ACCOUNT_ID
    )


if __name__ == "__main__":
    main()
