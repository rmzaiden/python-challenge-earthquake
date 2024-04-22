from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.city_schema import CityCreate, CityResponse
from services.city_service import create_city

city_router = APIRouter()


@city_router.post(
    "/v1/cities/", response_model=CityResponse, status_code=status.HTTP_201_CREATED
)
def add_city(city_create: CityCreate):
    try:
        # Chama a função de serviço que cria uma nova cidade
        city = create_city(city_create)
        return city
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
