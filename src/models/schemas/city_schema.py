from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    state_province_id: int

class CityResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
