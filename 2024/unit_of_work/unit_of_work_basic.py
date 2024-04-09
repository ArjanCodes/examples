from dataclasses import dataclass, field


@dataclass
class User:
    username: str


@dataclass
class UnitOfWork:
    new_users: list = field(default_factory=list)
    dirty_users: list = field(default_factory=list)
    removed_users: list = field(default_factory=list)

    def register_new(self, user: User) -> None:
        self.new_users.append(user)

    def register_dirty(self, user: User) -> None:
        if user not in self.dirty_users:
            self.dirty_users.append(user)

    def register_removed(self, user: User) -> None:
        self.removed_users.append(user)

    def commit(self) -> None:
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_users:
            # Insert new object into the database
            print(f"Inserting {obj}")
            # For demonstration, pretend we insert into a database here
        self.new_users.clear()

    def update_dirty(self):
        for obj in self.dirty_users:
            # Update existing object in the database
            print(f"Updating {obj}")
            # For demonstration, pretend we update in a database here
        self.dirty_users.clear()

    def delete_removed(self):
        for obj in self.removed_users:
            # Remove object from the database
            print(f"Deleting {obj}")
            # For demonstration, pretend we delete from a database here
        self.removed_users.clear()


def main() -> None:
    # Creating a new Unit of Work
    uow = UnitOfWork()

    # Creating a new user
    new_user = User("john_doe")
    uow.register_new(new_user)

    # Simulate updating a user
    existing_user = User("existing_user")
    uow.register_dirty(existing_user)

    # Simulate removing a user
    removed_user = User("removed_user")
    uow.register_removed(removed_user)

    # Committing changes
    uow.commit()


if __name__ == "__main__":
    main()
