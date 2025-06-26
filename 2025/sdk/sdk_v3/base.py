from typing import ClassVar, Type

from pydantic import BaseModel

from sdk_v3 import client


class BaseAPIModel[T: BaseAPIModel](BaseModel):
    id: str | None = None
    _resource_path: ClassVar[str] = ""

    def save(self) -> None:
        data = self.dict(exclude_unset=True)
        if self.id:
            response = client.put(f"/{self._resource_path}/{self.id}", json=data)
        else:
            response = client.post(f"/{self._resource_path}", json=data)
        response.raise_for_status()
        self.id = response.json()["id"]

    def delete(self) -> None:
        if not self.id:
            raise ValueError("Cannot delete unsaved resource.")
        response = client.delete(f"/{self._resource_path}/{self.id}")
        response.raise_for_status()

    @classmethod
    def load(cls: Type[T], resource_id: str) -> T:
        response = client.get(f"/{cls._resource_path}/{resource_id}")
        if response.status_code == 404:
            raise ValueError(f"{cls.__name__} not found.")
        response.raise_for_status()
        return cls(**response.json())

    @classmethod
    def find(cls: Type[T]) -> list[T]:
        response = client.get(f"/{cls._resource_path}")
        response.raise_for_status()
        return [cls(**item) for item in response.json()]
