from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from helper.database import Base


class City(Base):
    """
    Represents a city in the database.

    Attributes:
        id (int): The unique identifier for the city.
        name (str): The name of the city.
    """

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    state_province_id = Column(Integer, ForeignKey("states.id"))
    state = relationship("State", back_populates="cities")
    earthquake_searches = relationship("EarthquakeSearch", back_populates="city")
