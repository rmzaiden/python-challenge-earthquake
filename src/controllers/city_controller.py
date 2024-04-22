from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.city_schema import CityCreate, CityResponse
from services.city_service import create_city, get_cities

city_router = APIRouter()


@city_router.post(
    "/v1/cities/", response_model=CityResponse, status_code=status.HTTP_201_CREATED
)
def add_city(city_create: CityCreate):
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
        city = create_city(city_create)
        return city
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e
    
@city_router.get("/cities/", response_model=List[CityResponse])
def list_cities():
    """
    Retrieve a list of cities.

    Returns:
        List[str]: A list of city names.

    Raises:
        HTTPException: If there is a validation error (status code 400) or an unexpected error occurs (status code 500).
    """
    try:
        states = get_cities()
        return states
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e    
