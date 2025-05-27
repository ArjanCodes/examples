from sdk_v3.client import set_credentials
from sdk_v3.user import User


def main():
    # Initialize the API client with your API
    set_credentials(token="secret123")

    # Fetch users from the API
    users = User.find()
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
