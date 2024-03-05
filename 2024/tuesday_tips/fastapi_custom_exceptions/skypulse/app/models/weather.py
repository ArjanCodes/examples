from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from . import Base


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[int] = mapped_column(index=True)
    humidity: Mapped[int] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"), index=True, nullable=False
    )
    city = relationship("City", back_populates="weather_records")
