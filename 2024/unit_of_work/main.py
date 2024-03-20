from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session, declarative_base, Mapped
from typing import Optional
import contextlib

DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind = engine))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key = True)
    name: Mapped[str] = Column(String, unique = True, index = True)
    user_detail: Mapped['UserDetail'] = relationship('UserDetail', back_populates = 'user', uselist = False,
                                                     cascade = "all, delete-orphan")
    user_preference: Mapped['UserPreference'] = relationship('UserPreference', back_populates = 'user', uselist = False,
                                                             cascade = "all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class UserDetail(Base):
    __tablename__ = 'user_details'
    id: Mapped[int] = Column(Integer, primary_key = True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), unique = True)
    details: Mapped[str] = Column(String)
    user: Mapped['User'] = relationship('User', back_populates = 'user_detail')

    def __repr__(self) -> str:
        return f"UserDetail(id={self.id!r}, details={self.details!r})"


class UserPreference(Base):
    __tablename__ = 'user_preferences'
    id: Mapped[int] = Column(Integer, primary_key = True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), unique = True)
    preference: Mapped[str] = Column(String)
    user: Mapped['User'] = relationship('User', back_populates = 'user_preference')

    def __repr__(self) -> str:
        return f"UserPreference(id={self.id!r}, preference={self.preference!r})"


def create_user(session: Session, name: str, details: Optional[str] = None, preferences: Optional[str] = None) -> User:
    user = User(name = name)
    if details:
        user.user_detail = UserDetail(details = details)
    if preferences:
        user.user_preference = UserPreference(preference = preferences)
    session.add(user)
    return user


def update_user(session: Session, user_id: int, name: Optional[str] = None, details: Optional[str] = None,
                preferences: Optional[str] = None) -> Optional[User]:
    user: Optional[User] = session.get(User, user_id)
    if not user:
        return None
    if name:
        user.name = name
    if details:
        if user.user_detail:
            user.user_detail.details = details
        else:
            user.user_detail = UserDetail(details = details)
    if preferences:
        if user.user_preference:
            user.user_preference.preference = preferences
        else:
            user.user_preference = UserPreference(preference = preferences)
    return user


def delete_user(session: Session, user_id: int) -> None:
    user: Optional[User] = session.get(User, user_id)
    if user:
        session.delete(user)


def get_user(session: Session, user_id: int) -> Optional[User]:
    user: Optional[User] = session.get(User, user_id)
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
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def main():
    with unit() as session:
        user = create_user(session, "Arjan", "details", "preferences")
        print(user, user.user_detail, user.user_preference)
        session.flush()
        user = update_user(session, user.id, "Arjan Updated", "more details", "updated preferences")
        print(user, user.user_detail, user.user_preference)
        user = get_user(session, user.id)
        print(user)
        users = get_users(session)
        print(users)
        delete_user(session, user.id)
        users = get_users(session)
        print(users)


if __name__ == "__main__":
    main()
