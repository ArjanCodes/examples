from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Optional, Protocol


@dataclass
class UserRow:
    id: int = field(metadata={"pk": True})
    email: str
    age: Optional[int] = None


class DataclassLike(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


def to_sql_schema(cls: type[DataclassLike]) -> str:
    type_map: dict[type[Any], str] = {
        int: "INTEGER",
        str: "TEXT",
    }

    columns: list[str] = []

    for f in fields(cls):
        print(f.type)
        base = f.type if isinstance(f.type, type) else None
        sql_type = type_map.get(base, "TEXT") if base is not None else "TEXT"
        column = f"{f.name} {sql_type}"

        if f.metadata.get("pk"):
            column += " PRIMARY KEY"

        if f.default is None:
            column += " NULL"
        else:
            column += " NOT NULL"

        columns.append(column)

    table = cls.__name__.lower()
    return f"CREATE TABLE {table} (\n  " + ",\n  ".join(columns) + "\n);"


def main() -> None:
    print(to_sql_schema(UserRow))


if __name__ == "__main__":
    main()
