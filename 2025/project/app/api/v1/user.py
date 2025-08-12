from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


def get_user_service() -> UserService:
    return UserService(session=SessionLocal())


@router.get("/users", response_model=list[UserRead])
def get_users(service: UserService = Depends(get_user_service)):
    return service.list_users()


@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user.name)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, user: UserCreate, service: UserService = Depends(get_user_service)
):
    updated = service.update_user(user_id, user.name)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/users/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True}
