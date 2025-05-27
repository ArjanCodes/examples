from pydantic import BaseModel, EmailStr

from sdk_v2 import client


class User(BaseModel):
    id: str
    name: str
    email: EmailStr

    @classmethod
    def find(cls) -> list["User"]:
        response = client.get("/users")
        return [cls(**data) for data in response.json()]
