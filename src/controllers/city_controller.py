from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.city_schema import CityCreate, CityResponse
from services.city_service import create_city

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
