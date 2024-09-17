from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


# Define a model
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # user printing
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"


def main():
    # Database setup
    engine = create_engine("sqlite:///mydatabase.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a user
    new_user = User(name="Arjan")
    session.add(new_user)
    session.commit()

    # read all users
    users = session.query(User).all()
    print(users)


if __name__ == "__main__":
    main()
