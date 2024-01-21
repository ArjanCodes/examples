from datetime import datetime
from typing import Optional, Union
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, EmailStr, Field, field_serializer, UUID4

app = FastAPI()

class User(BaseModel):
    model_config = {
            "extra": "forbid",
    }
    __users__ = []
    name: str = Field(..., description="Name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    friends: list[UUID4] = Field(default_factory=list, max_items=500, description="List of friends")
    blocked: list[UUID4] = Field(default_factory=list, max_items=500, description="List of blocked users")
    signup_ts: Optional[datetime] = Field(default_factory=datetime.now, description="Signup timestamp", kw_only = True)
    id: UUID4 = Field(default_factory=uuid4, description="Unique identifier", kw_only = True)

    @field_serializer("id", when_used = "json")
    def serialize_id(self, id: UUID4) -> str:
        return str(id)    

@app.get("/users", response_model=list[User])
async def get_users() -> list[User]:
    return list(User.__users__)

@app.post("/users", response_model=User)
async def create_user(user: User):
    User.__users__.append(user)
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID4) -> Union[User, JSONResponse]:
    try:
        return next((user for user in User.__users__ if user.id == user_id))
    except StopIteration:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    

def main():
    with TestClient(app) as client:
        for i in range(5):
            response = client.post("/users", json={"name": f"User {i}", "email": f"example{i}@arjancodes.com"})
            assert response.status_code == 200
            assert response.json()["name"] == f"User {i}", "The name of the user should be User {i}"
            assert response.json()["id"], "The user should have an id"
            
            user =  User.model_validate(response.json())
            assert str(user.id) == response.json()["id"], "The id should be the same"
            assert user.signup_ts, "The signup timestamp should be set"
            assert user.friends == [], "The friends list should be empty"
            assert user.blocked == [], "The blocked list should be empty"
        
        response = client.get("/users")
        assert response.status_code == 200, "Response code should be 200"
        assert len(response.json()) == 5, "There should be 5 users"
        
        response = client.post("/users", json={"name": "User 5", "email": "example5@arjancodes.com"})
        assert response.status_code == 200
        assert response.json()["name"] == "User 5", "The name of the user should be User 5"
        assert response.json()["id"], "The user should have an id"
        
        user =  User.model_validate(response.json())
        assert str(user.id) == response.json()["id"], "The id should be the same"
        assert user.signup_ts, "The signup timestamp should be set"
        assert user.friends == [], "The friends list should be empty"
        assert user.blocked == [], "The blocked list should be empty"
        
        response = client.get(f"/users/{response.json()['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == "User 5", "This should be the newly created user"
        
        response = client.get(f"/users/{uuid4()}")
        assert response.status_code == 404
        assert response.json()["message"] == "User not found", "We technically should not find this user"

        response = client.post("/users", json={"name": "User 6", "email": "wrong"})
        assert response.status_code == 422, "The email address is should be invalid"
        
        
        
if __name__ == "__main__":
    main()