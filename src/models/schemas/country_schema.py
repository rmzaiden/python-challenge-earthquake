from pydantic import BaseModel


class CountryCreate(BaseModel):
    name: str


class CountryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
