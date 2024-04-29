from sqlalchemy import Column, Integer, String

from helper.database import Base


class Country(Base):
    """
    Represents a country in the database.

    Attributes:
        id (int): The unique identifier for the country.
        name (str): The name of the country.
    """
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
