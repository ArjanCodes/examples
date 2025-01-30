from typing import Any, Self
from pydantic import BaseModel, ConfigDict

from .client import http_delete, http_get, http_patch, http_post


class MoneybirdModel(BaseModel):
    id: int | None = None
    model_config = ConfigDict(extra="ignore")

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
        data = http_get(f"{self.endpoint}s/{id}")
        self.update(data)

    def save(self) -> None:
        if self.id is None:
            data = http_post(
                f"{self.endpoint}s",
                data={self.endpoint: self.to_dict()},
            )
            # update the current object with the data
            self.update(data)
        else:
            data = http_patch(
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
        http_delete(f"{self.endpoint}s/{self.id}")
        # remove the id from the object
        self.id = None

    @classmethod
    def find_by_id(cls: type[Self], id: int) -> Self:
        entity = cls(id=id)
        entity.load(id)
        return entity

    @classmethod
    def update_by_id(cls: type[Self], id: int, data: dict[str, Any]) -> Self:
        entity = cls(id=id)
        entity.update(data)
        entity.save()
        return entity

    @classmethod
    def delete_by_id(cls: type[Self], id: int) -> Self:
        entity = cls(id=id)
        entity.delete()
        return entity
