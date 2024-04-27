from pydantic import BaseModel


class StateCreate(BaseModel):
    name: str
    state_abbreviation: str
    country_id: int


class StateResponse(BaseModel):
    id: int
    name: str
    state_abbreviation: str
    country_id: int

    class Config:
        orm_mode = True
