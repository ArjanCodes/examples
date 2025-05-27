from pydantic import BaseModel, EmailStr

from .client import APIHttpClient


class User(BaseModel):
    id: str
    name: str
    email: EmailStr

    @classmethod
    def find(cls, client: APIHttpClient) -> list["User"]:
        response = client.get("/users")
        return [cls(**data) for data in response.json()]
