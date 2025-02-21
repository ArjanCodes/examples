from dataclasses import dataclass
from uuid import UUID, uuid4


# Custom exception for not found errors
class NotFoundError(Exception):
    pass


# User model using dataclass (id is now mandatory)
@dataclass
class User:
    id: UUID
    name: str
    age: int
    email: str


# In-memory sample data
sample_users: dict[str, User] = {
    "1": User(id=uuid4(), name="Alice", age=25, email="alice@example.com"),
    "2": User(id=uuid4(), name="Bob", age=30, email="bob@example.com"),
    "3": User(id=uuid4(), name="Charlie", age=25, email="charlie@example.com"),
}


# Get user by ID (raises exception if not found)
def get_user(user_id: str) -> User:
    user = sample_users.get(user_id)
    if not user:
        raise NotFoundError("User not found")
    return user


# Get users by filter (dynamically works with any filter key)
def get_users(filter: dict[str, str]) -> list[User]:
    # If no filter is provided, return all users
    if not filter:
        return list(sample_users.values())

    filtered_users = []

    # Loop through users and check filters dynamically
    for user in sample_users.values():
        match = True
        for key, value in filter.items():
            # Use getattr to dynamically check attributes
            user_value = getattr(user, key, None)
            if user_value is None or str(user_value) != value:
                match = False
                break  # No need to check further if one attribute doesn't match

        if match:
            filtered_users.append(user)

    return filtered_users


# Find user by email (returns None if not found)
def find_user_by_email(email: str) -> User | None:
    for user in sample_users.values():
        if user.email == email:
            return user
    return None  # Return None if no user is found


def main() -> None:
    # Get a user by ID (raises exception if not found)
    try:
        user_id = "1"  # Change this to test with different IDs
        user = get_user(user_id)
        print("User by ID:", user)
    except NotFoundError as e:
        print(e)

    # Get users by dynamic filter (works with any filter key)
    filters = {"age": "25"}  # Change this to test with different filters
    users = get_users(filters)
    print("Users by filter:", users)

    # Test with multiple filter criteria
    multiple_filters = {"age": "25", "name": "Alice"}
    users = get_users(multiple_filters)
    print("Users by multiple filters:", users)

    # Test with a non-existing attribute
    non_existing_filter = {"nonexistent": "value"}
    users = get_users(non_existing_filter)
    print("Users with non-existing filter:", users)


if __name__ == "__main__":
    main()
