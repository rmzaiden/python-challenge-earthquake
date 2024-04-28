from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from helper.database import Base

class EarthquakeSearch(Base):
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
