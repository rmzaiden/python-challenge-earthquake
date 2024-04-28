from pydantic import BaseModel, Field, field_validator


class CountryCreate(BaseModel):
    """
    Represents the schema for creating a country.

    Attributes:
        name (str): The name of the country.
    """

    name: str = Field(..., description="The name of the country.")

    @field_validator('name')
    def validate_name(cls, value):
        """
        Validates the country name.

        Args:
            value (str): The country name to be validated.

        Raises:
            ValueError: If the country name is empty or contains only spaces.

        Returns:
            str: The validated country name.
        """
        if not value.strip():
            raise ValueError('The country name must not be empty or just spaces.')
        return value
    
    class Config:
        orm_mode = True


class CountryResponse(BaseModel):
    """
    Represents a country response.

    Attributes:
        id (int): The ID of the country.
        name (str): The name of the country.
    """
    id: int
    name: str