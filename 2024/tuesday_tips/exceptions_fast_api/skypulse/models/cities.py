from sqlite3 import Cursor
from string import Template
from skypulse.schemas.city import City, CityData


def create(cursor: Cursor, params: CityData) -> City:
    city = City(**params)

    template = Template(
        "INSERT INTO cities (name, country, population) VALUES ('$name', '$country', '$population')"
    )

    query = template.substitute(
        name=city.name, country=city.country, population=city.population
    )

    cursor.execute(query)

    return cursor.fetchone()


def index(cursor: Cursor) -> list[City]:
    template = Template("SELECT * FROM cities")

    query = template.substitute()
    cursor.execute(query)
    cities = cursor.fetchall()

    return cities


def show(cursor: Cursor, city_id: int) -> City:
    template = Template("SELECT * FROM cities WHERE id = '$id'")

    query = template.substitute(id=city_id)
    cursor.execute(query)
    return cursor.fetchone()


def update(cursor: Cursor, city_id: int, params: CityData) -> City:
    template = Template("UPDATE cities SET name = '$name' WHERE id = $id")
    city = City(**params)
    query = template.substitute(
        id=city_id, name=city.name, country=city.country, population=city.population
    )
    cursor.execute(query)

    return cursor.fetchone()


def delete(cursor: Cursor, city_id: int) -> City:
    template = Template("DELETE FROM cities WHERE id = $id")
    query = template.substitute(id=city_id)
    cursor.execute(query, (city_id,))

    return cursor.fetchone()
