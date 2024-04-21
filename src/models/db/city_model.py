from sqlalchemy import Column, Integer, String

from helper.database import Base


class City(Base):
    """
    Represents a city in the database.

    Attributes:
        id (int): The unique identifier for the city.
        name (str): The name of the city.
        population (int): The population of the city.
    """

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    population = Column(Integer)
