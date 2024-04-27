from typing import List

from fastapi import APIRouter, HTTPException, status

from models.schemas.country_schema import CountryCreate, CountryResponse
from services.country_service import create_country, get_countries

country_router = APIRouter()


@country_router.post("/v1/countries/", response_model=CountryResponse)
def add_country(country_create: CountryCreate):
    """
    Adds a new country to the system.

    Args:
        country_create (CountryCreate): The data required to create a new country.

    Returns:
        Country: The newly created country.

    Raises:
        HTTPException: If an error occurs while creating the country.
    """
    try:
        country = create_country(country_create)
        return country
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e


@country_router.get("/v1/countries/", response_model=List[CountryResponse])
def list_countries():
    """
    Retrieve a list of countries.

    Returns:
        List[str]: A list of country names.

    Raises:
        HTTPException: If there is a client-side error (status code 400) or an unexpected error occurs (status code 500).
    """
    try:
        countries = get_countries()
        return countries
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e
