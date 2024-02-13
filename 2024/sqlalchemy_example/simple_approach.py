import sqlalchemy as sa
import atexit

engine = sa.create_engine('sqlite:///:memory:')
connection = engine.connect()

atexit.register(connection.close)
metadata = sa.MetaData()

user_table = sa.Table('user', metadata,
                      sa.Column('id', sa.Integer, primary_key=True),
                      sa.Column('username', sa.String),
                      sa.Column('email', sa.String),
                      )


def insert_user(username, email):
    query = user_table.insert().values(username=username, email=email)
    connection.execute(query)
    
def select_user(username):
    query = user_table.select().where(user_table.c.username == username)
    result = connection.execute(query)
    return result.fetchone()

def main():
    metadata.create_all(engine)
    insert_user("Arjan", "Arjan@arjancodes.com")
    print(select_user("Arjan"))
    
if __name__ == '__main__':
    main()
