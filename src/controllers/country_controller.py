from typing import List

from fastapi import APIRouter, HTTPException, status

from models.schemas.country_schema import CountryCreate, CountryResponse
from services.country_service import create_country, get_countries

country_router = APIRouter()


@country_router.post("/v1/countries/", response_model=CountryResponse)
def add_country(country_create: CountryCreate):
    try:
        country = create_country(country_create)
        return country
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@country_router.get("/countries/", response_model=List[CountryResponse])
def list_countries():
    countries = get_countries()
    return countries
