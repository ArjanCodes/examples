import sqlite3


class Model:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("tasks.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("create table if not exists tasks (title text)")

    def add_task(self, task: str) -> None:
        self.cursor.execute("insert into tasks values (?)", (task,))
        self.connection.commit()

    def delete_task(self, task: str) -> None:
        self.cursor.execute("delete from tasks where title = ?", (task,))
        self.connection.commit()

    def get_tasks(self) -> list[str]:
        tasks: list[str] = []
        for row in self.cursor.execute("select title from tasks"):
            tasks.append(row[0])
        return tasks
