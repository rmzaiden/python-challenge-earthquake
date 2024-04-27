from pydantic import BaseModel


class CityCreate(BaseModel):
    """
    Represents the schema for creating a city.

    Attributes:
        name (str): The name of the city.
        state_province_id (int): The ID of the state or province the city belongs to.
    """
    name: str
    state_province_id: int

class CityResponse(BaseModel):
    """
    Represents a city response.

    Attributes:
        id (int): The ID of the city.
        name (str): The name of the city.
    """

    id: int
    name: str

    class Config:
        """
        Configuration class for the CitySchema.

        Attributes:
            orm_mode (bool): Flag indicating whether the schema is used for ORM mode.
        """
        orm_mode = True
