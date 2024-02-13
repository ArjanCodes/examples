import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

db = sa.create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=db)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: int = sa.Column(sa.Integer, primary_key=True)
    username:str = sa.Column(sa.String)
    email: str = sa.Column(sa.String)
    
    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'
    
def main():
    Base.metadata.create_all(db)
    user = User(username='Arjan', email = "Arjan@arjancodes.com")
    
    with Session() as session:
        session.add(user)
        session.commit()
        print(session.query(User).all())
    
if __name__ == '__main__':
    main()