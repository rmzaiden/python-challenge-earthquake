from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.city_schema import CityCreate, CityResponse
from services.city_service import CityService

city_router = APIRouter()


def get_city_service():
    """
    Returns an instance of the CityService class.

    :return: CityService instance
    """
    return CityService()


@city_router.post(
    "/v1/cities/", response_model=CityResponse, status_code=status.HTTP_201_CREATED
)
def add_city(
    city_create: CityCreate, city_service: CityService = Depends(get_city_service)
):
    """
    Add a new city to the system.

    Args:
        city_create (CityCreate): The data required to create a new city.

    Returns:
        City: The newly created city.

    Raises:
        HTTPException: If there is a validation error or an unexpected error occurs.
    """
    try:
        city = city_service.create_city(city_create)
        return city
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e


@city_router.get("/v1/cities/", response_model=List[CityResponse])
def list_cities(city_service: CityService = Depends(get_city_service)):
    """
    Retrieve a list of cities.

    Returns:
        List[CityResponse]: A list of city responses.

    Raises:
        HTTPException: If there is a validation error (status code 400) or an unexpected error occurs (status code 500).
    """
    try:
        cities = city_service.get_cities()
        return cities
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        ) from e
