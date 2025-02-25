from dataclasses import dataclass

type JSONDict = dict[str, str | int | float | bool | None]


@dataclass
class APIClient:
    api_url: str
    api_version_id: str
    account_id: int
    token: str

    def _make_request(
        self, path: str, data: JSONDict | None = None, method: str = "post"
    ) -> None:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        fullpath = f"{self.api_url}/{self.api_version_id}/{self.account_id}/{path}"
        print(f"Making request to {fullpath}")
        print(f"Data: {data}")
        print(f"Method: {method}")
        print(f"Headers: {headers}")

    def post(self, path: str, data: JSONDict | None = None) -> None:
        self._make_request(path, data, "post")

    def get(self, path: str) -> None:
        self._make_request(path, method="get")

    def patch(self, path: str, data: JSONDict | None = None) -> None:
        self._make_request(path, data, "patch")

    def delete(self, path: str) -> None:
        self._make_request(path, method="delete")


API_URL = "https://api.company.com"
API_VERSION_ID = "v2"
TOKEN = "a3f5c7e8d9b1c2e3f4a5b62e3f4a5b6c7d8e9f0a1"
ACCOUNT_ID = 98753244984


def main() -> None:
    client = APIClient(API_URL, API_VERSION_ID, ACCOUNT_ID, TOKEN)
    client.post("invoices", {"amount": 1000})
    client.get("invoices")
    client.patch("invoices", {"amount": 2000})
    client.delete("invoices")


if __name__ == "__main__":
    main()
