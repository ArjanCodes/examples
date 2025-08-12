from sqlalchemy.orm import Session

from app.db.schema import User


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def list_users(self) -> list[User]:
        return self._db.query(User).all()

    def get_user(self, user_id: int) -> User | None:
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, name: str) -> User:
        user = User(name=name)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, name: str) -> User | None:
        user = self.get_user(user_id)
        if not user:
            return None
        user.name = name
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
