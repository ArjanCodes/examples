from decimal import Decimal
from string import Template
from typing import Any
from employee_portal.database.database import DatabaseConnector
from employee_portal.position import Position

DATABASE = "./examples.db"

def create(
    connector: DatabaseConnector, name: str, position: Position, salary: Decimal
):
    conn = connector.connect(DATABASE)
    cursor = connector.create_cursor(conn)

    try:
        template = Template(
            "INSERT INTO employees (name, position, salary) VALUES ('$name', '$position', $salary)"
        )

        query = template.substitute(name=name, position=position.value, salary=salary)

        print(query)
        cursor.execute(query)

        conn.commit()

        print("Record inserted successfully")

    finally:
        connector.close_connection(conn)


def index(connector: DatabaseConnector):
    conn = connector.connect(DATABASE)
    cursor = connector.create_cursor(conn)
    try:
        template = Template("SELECT * FROM employees")

        query = template.substitute()
        cursor.execute(query)
        employees = cursor.fetchall()

        return employees

    finally:
        connector.close_connection(conn)


def show(connector: DatabaseConnector, employee_id: int) -> tuple[Any, Any]:
    conn = connector.connect(DATABASE)
    cursor = connector.create_cursor(conn)

    try:
        template = Template("SELECT * FROM employees WHERE id = '$id'")

        query = template.substitute(id=employee_id)
        cursor.execute(query)
        employee = cursor.fetchone()
        return employee

    finally:
        connector.close_connection(conn)


def update(
    connector: DatabaseConnector,
    employee_id: int,
    name: str,
    position: Position,
    salary: Decimal,
) -> None:
    conn = connector.connect(DATABASE)
    cursor = connector.create_cursor(conn)

    try:
        template = Template(
            "UPDATE employees SET name = '$name', position = '$position', salary = '$salary' WHERE id = $id"
        )
        query = template.substitute(
            name=name, position=position.value, salary=salary, id=employee_id
        )
        cursor.execute(query)

        conn.commit()

        print(f"Employee with ID {employee_id} updated successfully")

    finally:
        connector.close_connection(conn)


def delete(connector: DatabaseConnector, employee_id: int) -> None:
    conn = connector.connect(DATABASE)
    cursor = connector.create_cursor(conn)

    try:
        template = Template("DELETE FROM employees WHERE id = $id")
        query = template.substitute(id=employee_id)
        cursor.execute(query, (employee_id,))

        conn.commit()

        print(f"Employee with ID {employee_id} deleted successfully")

    finally:
        connector.close_connection(conn)
