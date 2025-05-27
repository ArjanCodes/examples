from sdk_v3.client import set_credentials
from sdk_v3.user import User


def main():
    # Initialize the API client with your API
    set_credentials(token="secret123")

    # Create and save
    u = User(name="Alice", email="alice@example.com")
    u.save()

    # Change and save
    u.name = "Alice Smith"
    u.save()

    # Find all users
    users = User.find()
    print(users)


if __name__ == "__main__":
    main()
