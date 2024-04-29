from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from helper.database import Base

class EarthquakeSearch(Base):
    """
    Represents a search for earthquakes in a specific city.

    Attributes:
        id (int): The unique identifier for the earthquake search.
        city_id (int): The ID of the city associated with the search.
        city (City): The city associated with the search.
        start_date (datetime): The start date of the search.
        end_date (datetime): The end date of the search.
        closest_earthquake_date (datetime): The date of the closest earthquake found in the search.
        closest_earthquake_magnitude (float): The magnitude of the closest earthquake found in the search.
        closest_earthquake_distance (float): The distance to the closest earthquake found in the search.
        closest_earthquake_location (str): The location of the closest earthquake found in the search.
    """

    __tablename__ = 'earthquake_searches'
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship("City", back_populates="earthquake_searches")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    closest_earthquake_date = Column(DateTime)
    closest_earthquake_magnitude = Column(Float)
    closest_earthquake_distance = Column(Float)
    closest_earthquake_location = Column(String(255))
