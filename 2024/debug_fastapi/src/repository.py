from datetime import datetime
from datetime import timezone
from typing import Any, Literal
from uuid import UUID
from uuid import uuid4
from src.models import CoreModel

FAKE_DB = {"customers": {}, "payments": {}}

type ResourceType = Literal["customers", "payments"]


async def get_resource(id: UUID, resource_type: ResourceType) -> CoreModel | None:
    # Dynamically fetch resource from the "FAKE_DB" by resource type
    resources = FAKE_DB.get(resource_type)

    if not resources:
        raise ValueError(f"Resource type {resource_type} does not exist")

    resource = resources.get(id)

    if resource:
        return resource

    raise ValueError(f"Resource {id} does not exist in {resource_type}")


async def get_resources(resource_type: ResourceType) -> list[CoreModel] | None:
    # Dynamically fetch all resources of a specific type from the "FAKE_DB"
    resources = FAKE_DB.get(resource_type)

    if resources is None:
        raise ValueError(f"Resource type {resource_type} does not exist")

    return resources.values()


async def create_resource(
    resource_type: ResourceType, params: dict[str, Any]
) -> CoreModel:
    # Create a new resource and add it to the "FAKE_DB"
    id = uuid4()

    resources = FAKE_DB.get(resource_type)

    if not resources:
        raise ValueError(f"Resource type {resource_type} does not exist")

    new_resource = {
        "id": uuid4(),
        "inserted_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        **params,
    }
    resources[id] = new_resource
    return new_resource


async def update_resource(
    id: UUID, resource_type: ResourceType, params: dict[str, Any]
) -> CoreModel | None:
    # Update an existing resource in the "FAKE_DB"
    resource = await get_resource(id, resource_type)

    if resource:
        resource.update(params)
        resource["updated_at"] = datetime.now(timezone.utc)  # Update the timestamp
        return resource

    raise ValueError(f"Resource {id} does not exist in {resource_type}")
