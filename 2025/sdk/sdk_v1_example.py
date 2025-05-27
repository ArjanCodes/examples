from sdk_v1.client import APIHttpClient
from sdk_v1.user import User


def main():
    # Initialize the API client with your API
    client = APIHttpClient(token="secret123")

    # Fetch users from the API
    users = User.find(client)
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
