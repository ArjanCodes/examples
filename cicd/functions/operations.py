import sqlite3
from pathlib import Path
from typing import Any


class ChannelNotFoundError(Exception):
    pass


def get_channel(channel_id: str, db_path: str = "channels.db") -> dict[str, Any]:
    print(db_path)
    print(f"Working directory: {Path.cwd()}")
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM channels WHERE id = ?",
            (channel_id,),
        )
        channel = cursor.fetchone()
        print(channel)
        if channel is None:
            raise ChannelNotFoundError()
        return {
            "id": channel[0],
            "name": channel[1],
            "tags": channel[2].split(","),
            "description": channel[3],
        }
