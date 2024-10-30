from dataclasses import dataclass

from returns.maybe import Maybe, Nothing, Some


@dataclass
class User:
    id: int
    name: str


USERS = {1: User(1, "Alice"), 2: User(2, "Bob")}


# Using a Maybe container to handle optional values
def find_user(user_id) -> Maybe[User]:
    return Some(USERS[user_id]) if user_id in USERS else Nothing


result = find_user(1).map(lambda user: user.name)
print(result)  # Some('Alice')

missing_result = find_user(3).map(lambda user: user.name)
print(missing_result)  # Nothing
