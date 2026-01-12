from __future__ import annotations

from pymongo.asynchronous.database import AsyncDatabase

MONGODB_URI = "mongodb://root:example@localhost:27017/?authSource=admin"
DATABASE_NAME = "cqrs_demo"
TICKETS_COLL = "tickets"

mongo_client = AsyncMongoClient(MONGODB_URI)
db: AsyncDatabase | None = None


def get_db() -> AsyncDatabase:
    return mongo_client[DATABASE_NAME]


def shutdown_db() -> None:
    mongo_client.close()
