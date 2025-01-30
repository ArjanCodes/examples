from pydantic import BaseModel
from .model import MoneybirdModel


class CustomField(BaseModel):
    id: int | None = None
    value: str | None = None


class CustomFieldModel(MoneybirdModel):
    custom_fields: list[CustomField] = []

    def get_custom_field(self, field_id: int) -> str | None:
        for field in self.custom_fields:
            if field.id == field_id:
                return field.value
        return None

    def set_custom_field(self, field_id: int, value: str) -> None:
        for field in self.custom_fields:
            if field.id == field_id:
                field.value = value
                return
        self.custom_fields.append(CustomField(id=field_id, value=value))
