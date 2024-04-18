from pydantic import BaseModel, Field


class WeatherBase(BaseModel):
    city_id: int
    temperature: int
    humidity: int = Field(gt=0, description="The price must be greater than zero")
    description: str = Field(
        max_length=255, description="The description must be less than 255 characters"
    )


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(WeatherBase):
    pass


class Weather(WeatherBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True
