import json

from pydantic import BaseModel, ConfigDict, Field


class Crop(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int = Field(0, ge=0)
    y: int = Field(0, ge=0)
    width: int = Field(0, ge=0)
    height: int = Field(0, ge=0)

    # Since we are using formdata to send the data, we need to override the default
    # pydantic behaviour of converting the data to json
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
