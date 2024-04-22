from pydantic import BaseModel


class StateCreate(BaseModel):
    name: str
    country_id: int


class StateResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
