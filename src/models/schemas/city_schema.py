from pydantic import BaseModel, Field, field_validator


class CityCreate(BaseModel):
    """
    Represents the schema for creating a city.

    Attributes:
        name (str): The name of the city.
        state_province_id (int): The ID of the state or province the city belongs to.
    """

    name: str = Field(..., description="The name of the city.")
    state_province_id: int = Field(..., description="The ID of the state or province the city belongs to.")

    @field_validator('name')
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError('The city name must not be empty or just spaces.')
        return value


class CityResponse(BaseModel):
    """
    Represents a city response.

    Attributes:
        id (int): The ID of the city.
        name (str): The name of the city.
    """

    id: int
    name: str
    state_province_id: int
