from pydantic import BaseModel, Field, field_validator


class StateCreate(BaseModel):
    """
    Represents the schema for creating a state or province.

    Atributes: 
        name (str): The name of the state or province.
        state_abbreviation (str): The abbreviation of the state or province.
        country_id (int): The ID of the country the state or province belongs to.
    """

    name: str = Field(..., description="The name of the state or province.")
    state_abbreviation: str = Field(..., description="The abbreviation of the state or province.")
    country_id: int = Field(..., description="The ID of the country the state or province belongs to.")


    @field_validator('name')
    def validate_name(cls, value):
            """
            Validates the state name.

            Args:
                value (str): The state name to be validated.

            Raises:
                ValueError: If the state name is empty or contains only spaces.

            Returns:
                str: The validated state name.
            """
            if not value.strip():
                raise ValueError('The state name must not be empty or just spaces.')
            return value

    @field_validator('state_abbreviation')
    def validate_state_abbreviation(cls, value):
            """
            Validates the state abbreviation.

            Args:
                value (str): The state abbreviation to be validated.

            Raises:
                ValueError: If the state abbreviation is empty or contains only spaces.

            Returns:
                str: The validated state abbreviation.
            """
            if not value.strip():
                raise ValueError('The state abbreviation must not be empty or just spaces.')
            return value
    
    
    class Config:
            orm_mode = True


class StateResponse(BaseModel):
    """
    Represents a response object for a state.

    Attributes:
        id (int): The ID of the state.
        name (str): The name of the state.
        state_abbreviation (str): The abbreviation of the state.
        country_id (int): The ID of the country to which the state belongs.
    """

    id: int
    name: str
    state_abbreviation: str
    country_id: int