import httpx


def fetch_joke() -> str:
    """Fetch a random Chuck Norris joke from the API."""
    with httpx.Client() as client:
        response = client.get("https://api.chucknorris.io/jokes/random")
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return data["value"]


def main() -> None:
    print(fetch_joke())


if __name__ == "__main__":
    main()
