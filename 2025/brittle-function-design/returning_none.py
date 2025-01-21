import os
from typing import Any
from uuid import uuid4, UUID
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")


class NotFoundError(Exception):
    pass


class User(BaseModel):
    id: UUID = Field(
        default_factory=uuid4, alias="_id"
    )  # Nice way to handle _id convention in MongoDB
    name: str = Field(...)
    age: int = Field(...)
    email: str = Field(...)


def get_client() -> MongoClient[dict[str, Any]]:
    return MongoClient(CONNECTION_URL, connect=False)


def get_collection(
    collection_name: str, client: MongoClient[dict[str, Any]] = get_client()
) -> Collection[dict[str, Any]]:
    return client.get_database("test").get_collection(collection_name)


def get(id: str, collection: Collection[dict[str, Any]]) -> dict[str, Any]:
    obj_id = ObjectId(id)

    document = collection.find_one({"_id": obj_id})

    if not document:
        raise NotFoundError("User not found")

    return document


def index(
    filter: dict[str, str], collection: Collection[dict[str, Any]]
) -> list[dict[str, Any]]:
    documents = list(collection.find(filter))
    return documents


def get_user(
    user_id: str, collection: Collection[dict[str, Any]] = get_collection("users")
) -> User:
    user = get(user_id, collection)

    return User(**user)


def get_users(
    filter: dict[str, str],
    collection: Collection[dict[str, Any]] = get_collection("users"),
) -> list[User]:
    documents = index(filter, collection)
    return [User(**doc) for doc in documents]


def main() -> None:
    user_id = "60f7b4f3d1b3f3b3b3b3b3b3"

    user = get_user(user_id)

    print("User:", user)

    filters = {"age": "25"}  # Replace with your filter criteria

    users = get_users(filters)

    print("Users:", users)


# Example Usage
if __name__ == "__main__":
    main()
