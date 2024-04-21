from datetime import date

from pydantic import BaseModel, Field


class EarthquakeModel(BaseModel):
    """
    Represents a model for querying earthquake data.

    Attributes:
        city_name (str): Name of the city to check for earthquakes.
        start_date (date): Start date for the earthquake query in YYYY-MM-DD format.
        end_date (date): End date for the earthquake query in YYYY-MM-DD format.
    """

    city_name: str = Field(
        ...,
        example="Los Angeles, CA",
        description="Name of the city to check for earthquakes",
    )
    start_date: date = Field(
        ...,
        example="2021-06-01",
        description="Start date for the earthquake query in YYYY-MM-DD format",
    )
    end_date: date = Field(
        ...,
        example="2021-07-05",
        description="End date for the earthquake query in YYYY-MM-DD format",
    )


class EarthquakeResponse(BaseModel):
    """
    Represents the response object for an earthquake.

    Attributes:
        message (str): The message associated with the earthquake response.
    """

    message: str
