import json
from typing import Any, Optional

from sqlalchemy import String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    validates,
)


class Base(DeclarativeBase):
    custom_data: Mapped[Optional[str]]

    @validates("custom_data")
    def validate_custom_data(self, _: str, custom_data: Any) -> str:
        if not custom_data:
            return "{}"
        elif isinstance(custom_data, dict):
            return json.dumps(custom_data)
        else:
            return custom_data

    def update_item(self, key: str, value: Any) -> None:
        if value is None:
            return
        if key == "custom_data":
            self.update_custom_data(value)
        else:
            setattr(self, key, value)

    def update(self, data: dict[str, Any]) -> None:
        for key, value in data.items():
            self.update_item(key, value)

    def update_custom_data(self, custom_data: dict[str, Any]) -> None:
        # create JSON of current custom_data
        custom_data_json = json.loads(self.custom_data or "{}")
        # unset keys with value None and update the rest
        for k, v in custom_data.items():
            if v is None:
                custom_data_json.pop(k, None)
            else:
                custom_data_json[k] = v
        # convert back to string
        setattr(self, "custom_data", json.dumps(custom_data_json))

    def dict(self) -> dict[str, Any]:
        export_dict: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            elif key == "custom_data":
                export_dict[key] = json.loads(value)
            else:
                export_dict[key] = value
        return export_dict


class DBUser(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
