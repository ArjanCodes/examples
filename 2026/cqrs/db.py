from typing import Any, Mapping

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient

MONGODB_URI = "mongodb://root:example@localhost:27017/?authSource=admin"
DATABASE_NAME = "cqrs_demo"

type Database = AsyncDatabase[Mapping[str, Any]]
mongo_client = AsyncMongoClient[Mapping[str, Any]](MONGODB_URI)
db: Database | None = None


def get_db() -> Database:
    return mongo_client[DATABASE_NAME]


async def shutdown_db() -> None:
    await mongo_client.close()


def oid_str(oid: ObjectId) -> str:
    return str(oid)


def parse_object_id(ticket_id: str) -> ObjectId:
    return ObjectId(ticket_id)
