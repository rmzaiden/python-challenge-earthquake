from pydantic import BaseModel, Field
from datetime import date

class EarthquakeModel(BaseModel):
    city_name: str = Field(..., example="Los Angeles, CA", description="Name of the city to check for earthquakes")
    start_date: date = Field(..., example="2021-06-01", description="Start date for the earthquake query in YYYY-MM-DD format")
    end_date: date = Field(..., example="2021-07-05", description="End date for the earthquake query in YYYY-MM-DD format")
