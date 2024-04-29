from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.country_schema import CountryCreate, CountryResponse
from services.country_service import CountryService

country_router = APIRouter()


def get_country_service():
    """
    Dependency injector function that creates an instance of the CountryService class.
    """
    return CountryService()


@country_router.post(
    "/v1/countries/",
    response_model=CountryResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_country(
    country_create: CountryCreate,
    country_service: CountryService = Depends(get_country_service),
):
    """
    Adds a new country to the system.

    Args:
        country_create (CountryCreate): The data required to create a new country.
        country_service (CountryService): The service instance to handle country creation.

    Returns:
        Country: The newly created country.

    Raises:
        HTTPException: If an error occurs while creating the country.
    """
    try:
        country = country_service.create_country(country_create)
        return country
    except ValueError as e: #pragma: no cover
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e: #pragma: no cover
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred {e}"
        ) from e


@country_router.get("/v1/countries/", response_model=List[CountryResponse])
def list_countries(country_service: CountryService = Depends(get_country_service)):
    """
    Retrieve a list of countries.

    Returns:
        List[CountryResponse]: A list of countries.

    Raises:
        HTTPException: If there is a client-side error (status code 400) or an unexpected error occurs (status code 500).
    """
    try:
        countries = country_service.get_countries()
        return countries
    except ValueError as e: #pragma: no cover
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e: #pragma: no cover
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        ) from e
