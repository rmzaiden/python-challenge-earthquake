from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    population: int


class CityResponse(BaseModel):
    id: int
    name: str
    population: int

    class Config:
        orm_mode = True
