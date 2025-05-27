from typing import Optional
from uuid import uuid4

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Simulated database
fake_users_db = {}

# API key setup
API_KEY = "secret123"  # You can change this to anything you like


def get_api_key(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Authorization header",
        )

    token = authorization.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )

    return token


# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(UserCreate):
    id: str


# CRUD Endpoints
@app.post("/users", response_model=User)
def create_user(user: UserCreate, api_key: str = Depends(get_api_key)):
    user_id = str(uuid4())
    new_user = User(id=user_id, **user.dict())
    fake_users_db[user_id] = new_user
    return new_user


@app.get("/users", response_model=list[User])
def get_users(api_key: str = Depends(get_api_key)):
    return list(fake_users_db.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, api_key: str = Depends(get_api_key)):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(
    user_id: str, user_update: UserCreate, api_key: str = Depends(get_api_key)
):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User(id=user_id, **user_update.dict())
    fake_users_db[user_id] = updated_user
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(user_id: str, api_key: str = Depends(get_api_key)):
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_users_db[user_id]
    return {"detail": "User deleted"}


def main():
    uvicorn.run("test_api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
