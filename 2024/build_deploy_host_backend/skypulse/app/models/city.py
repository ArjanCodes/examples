from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.weather import Weather

from . import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[int] = mapped_column(index=True)
    country: Mapped[str] = mapped_column(index=True)
    population: Mapped[str] = mapped_column(nullable=True)
    weather_records: Mapped[list[Weather]] = relationship(
        "Weather", back_populates="city"
    )
