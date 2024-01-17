from sqlite3 import Cursor
from string import Template
from skypulse.schemas.storm import Storm, StormData


def index(cursor: Cursor) -> list[Storm]:
    template = Template("SELECT * FROM storms")
    query = template.substitute()
    cursor.execute(query)
    return cursor.fetchall()


def show(cursor: Cursor, storm_id: int) -> Storm:
    template = Template("SELECT * FROM storms WHERE id = '$id'")
    query = template.substitute(id=storm_id)
    cursor.execute(query)
    return cursor.fetchone()


def create(cursor: Cursor, params: StormData) -> Storm:
    storm = Storm(**params)
    template = Template(
        "INSERT INTO storms (name, type, severity) VALUES ('$name', '$type', '$severity')"
    )
    query = template.substitute(
        name=storm.name, type=storm.type, severity=storm.severity
    )
    cursor.execute(query)
    return cursor.fetchone()


def update(cursor: Cursor, storm_id: int, params: StormData) -> Storm:
    storm = Storm(**params)
    template = Template(
        "UPDATE storms SET name = '$name', type = '$type', severity = '$severity' WHERE id = $id"
    )
    query = template.substitute(
        id=storm_id, name=storm.name, type=type, severity=storm.severity
    )
    cursor.execute(query)
    return cursor.fetchone()


def delete(cursor: Cursor, storm_id: int) -> Storm:
    template = Template("DELETE FROM storms WHERE id = $id")
    query = template.substitute(id=storm_id)
    cursor.execute(query)
    return cursor.fetchone()
