class DatabaseConnection:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def __enter__(self):
        self.connection = connect(self.host, self.username, self.password)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def main() -> None:
    with DatabaseConnection("localhost", "myuser", "mypassword") as db:
        # Perform database operations
        db.query("SELECT * FROM users")
        # Connection is automatically closed at the end of the 'with' block


if __name__ == "__main__":
    main()
