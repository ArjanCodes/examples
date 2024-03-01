import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

db = sa.create_engine('sqlite:///:memory:')
Session = sessionmaker(bind = db)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    username: str = sa.Column(sa.String)
    email: str = sa.Column(sa.String)

    def __repr__(self) -> str:
        return f'<User(username={self.username}, email={self.email})>'


def main() -> None:
    Base.metadata.create_all(db)
    user = User(username = 'Arjan', email = "Arjan@arjancodes.com")

    with Session() as session:
        session.add(user)
        session.commit()
        print(session.query(User).all())


if __name__ == '__main__':
    main()
