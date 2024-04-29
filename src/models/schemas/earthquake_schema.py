from pydantic import BaseModel, Field


class EarthquakeModel(BaseModel):
    """
    Represents the schema for earthquake data.

    Attributes:
        city_name (str): Name of the city to check for earthquakes.
        city_id (int): ID of the city to check for earthquakes.
        state_abbreviation (str): State abbreviation of the city to check for earthquakes.
        start_date (str): Start date for the earthquake query in YYYY-MM-DD format.
        end_date (str): End date for the earthquake query in YYYY-MM-DD format.
    """
    city_name: str = Field(
        ...,
        example="Los Angeles",
        description="Name of the city to check for earthquakes",
    )
    city_id: int = Field(
        ...,
        example=1,
        description="ID of the city to check for earthquakes",
    )
    state_abbreviation: str = Field(
        ...,
        example="CA",
        description="State abbreviation of the city to check for earthquakes",
    )
    start_date: str = Field(
        ...,
        example="2021-06-01",
        description="Start date for the earthquake query in YYYY-MM-DD format",
    )
    end_date: str = Field(
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
