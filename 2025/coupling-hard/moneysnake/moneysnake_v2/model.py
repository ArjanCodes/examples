from typing import Any, Self
from pydantic import BaseModel, ConfigDict

from .client import MoneybirdClient


class MoneybirdModel(BaseModel):
    id: int | None = None
    model_config = ConfigDict(extra="ignore")
    client: MoneybirdClient

    @property
    def endpoint(self) -> str:
        return "".join(
            [
                "_" + letter.lower() if letter.isupper() else letter
                for letter in self.__class__.__name__
            ]
        ).lstrip("_")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)

    def load(self, id: int) -> None:
        data = self.client.http_get(f"{self.endpoint}s/{id}")
        self.update(data)

    def save(self) -> None:
        if self.id is None:
            data = self.client.http_post(
                f"{self.endpoint}s",
                data={self.endpoint: self.to_dict()},
            )
            # update the current object with the data
            self.update(data)
        else:
            data = self.client.http_patch(
                f"{self.endpoint}s/{self.id}",
                data={self.endpoint: self.to_dict()},
            )
            self.update(data)

    def update(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        if not self.id:
            raise ValueError(f"Cannot delete {self.__class__.__name__} without an id")
        self.client.http_delete(f"{self.endpoint}s/{self.id}")
        # remove the id from the object
        self.id = None

    @classmethod
    def find_by_id(cls: type[Self], client: MoneybirdClient, id: int) -> Self:
        entity = cls(client=client, id=id)
        entity.load(id)
        return entity

    @classmethod
    def update_by_id(
        cls: type[Self], client: MoneybirdClient, id: int, data: dict[str, Any]
    ) -> Self:
        entity = cls(client=client, id=id)
        entity.update(data)
        entity.save()
        return entity

    @classmethod
    def delete_by_id(cls: type[Self], client: MoneybirdClient, id: int) -> Self:
        entity = cls(client=client, id=id)
        entity.delete()
        return entity
