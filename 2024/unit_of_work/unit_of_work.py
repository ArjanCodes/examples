import contextlib
from typing import Optional

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
    scoped_session,
    sessionmaker,
)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, unique=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column()
    user_detail: Mapped["UserDetail"] = relationship(
        "UserDetail", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_preference: Mapped["UserPreference"] = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class UserDetail(Base):
    __tablename__ = "user_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    details: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship("User", back_populates="user_detail")

    def __repr__(self) -> str:
        return f"UserDetail(id={self.id!r}, details={self.details!r})"


class UserPreference(Base):
    __tablename__ = "user_preferences"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    preference: Mapped[str] = mapped_column(String)
    user: Mapped["User"] = relationship("User", back_populates="user_preference")

    def __repr__(self) -> str:
        return f"UserPreference(id={self.id!r}, preference={self.preference!r})"


def create_user(
    session: Session,
    name: str,
    details: Optional[str] = None,
    preferences: Optional[str] = None,
) -> User:
    user = User(name=name)
    if details:
        user.user_detail = UserDetail(details=details)
    if preferences:
        user.user_preference = UserPreference(preference=preferences)
    session.add(user)
    return user


def update_user(
    session: Session,
    user_id: int,
    name: Optional[str] = None,
    details: Optional[str] = None,
    preferences: Optional[str] = None,
) -> User:
    user: Optional[User] = session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    if name:
        user.name = name
    if details:
        if user.user_detail:
            user.user_detail.details = details
        else:
            user.user_detail = UserDetail(details=details)
    if preferences:
        if user.user_preference:
            user.user_preference.preference = preferences
        else:
            user.user_preference = UserPreference(preference=preferences)
    return user


def delete_user(session: Session, user_id: int) -> None:
    user: Optional[User] = session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    session.delete(user)


def get_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    return user


def get_users(session: Session) -> list[User]:
    users: list[User] = session.query(User).all()
    return users


Base.metadata.create_all(engine)


@contextlib.contextmanager
def unit():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print("Rolling back")
        session.rollback()
        raise e
    finally:
        session.close()


def main() -> None:
    try:
        with unit() as session:
            user = create_user(session, "Arjan", "details", "preferences")
            print(user, user.user_detail, user.user_preference)
            session.flush()
            print(user)
            user = update_user(
                session, 1, "Arjan Updated", "more details", "updated preferences"
            )
            print(user, user.user_detail, user.user_preference)
            user = get_user(session, user.id)
            print(user)
            delete_user(session, 1)
    except ValueError as e:
        print(e)

    with unit() as session:
        users = get_users(session)
        print(users)


if __name__ == "__main__":
    main()
