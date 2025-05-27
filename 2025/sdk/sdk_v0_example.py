import httpx


def main() -> None:
    # Initialize the API client with your API
    headers = {"Authorization": "Bearer secret123"}
    response = httpx.get("http://localhost:8000/users", headers=headers)
    users = response.json()
    print(users)


if __name__ == "__main__":
    main()
