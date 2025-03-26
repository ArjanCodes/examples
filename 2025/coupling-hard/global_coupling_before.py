API_URL = "https://api.company.com"
API_VERSION_ID = "v2"
TOKEN = "a3f5c7e8d9b1c2e3f4a5b62e3f4a5b6c7d8e9f0a1"
ACCOUNT_ID = 98753244984

type JSONDict = dict[str, str | int | float | bool | None]


def make_request(path: str, data: JSONDict | None = None, method: str = "post") -> None:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    fullpath = f"{API_URL}/{API_VERSION_ID}/{ACCOUNT_ID}/{path}"
    print(f"Making request to {fullpath}")
    print(f"Data: {data}")
    print(f"Method: {method}")
    print(f"Headers: {headers}")


def main() -> None:
    make_request("invoices", {"amount": 1000}, "post")


if __name__ == "__main__":
    main()
