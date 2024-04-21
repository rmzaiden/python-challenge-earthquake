from pydantic import BaseModel

class EarthquakeResponse(BaseModel):
    message: str