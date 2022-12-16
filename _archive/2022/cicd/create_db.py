import sqlite3

CHANNELS = [
    {
        "id": "codestackr",
        "name": "codeSTACKr",
        "tags": "web development,typescript",
        "description": "My tutorials are generally about web development and include coding languages such as HTML, CSS, Sass, JavaScript, and TypeScript.",
    },
    {
        "id": "jackherrington",
        "name": "Jack Herrington",
        "tags": "frontend,technology",
        "description": "Frontend videos from basic to very advanced; tutorials, technology deep dives. You'll love it!",
    },
    {
        "id": "arjancodes",
        "name": "ArjanCodes",
        "tags": "software design,python",
        "description": "ArjanCodes focuses on helping you become a better software developer.",
    },
]


def main() -> None:
    connection = sqlite3.connect("channels.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS channels (
            id TEXT PRIMARY KEY,
            name TEXT,
            tags TEXT,
            description TEXT
        )
        """
    )
    cursor.executemany(
        """
        INSERT INTO channels (id, name, tags, description)
        VALUES (:id, :name, :tags, :description)
        """,
        CHANNELS,
    )
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
