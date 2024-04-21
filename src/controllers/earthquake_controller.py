from fastapi import APIRouter, Depends, HTTPException
from models.earthquake_model import EarthquakeModel
from services.earthquake_service import EarthquakeService

router = APIRouter()

@router.get("/earthquake/", response_model=str)
async def get_closest_earthquake(query: EarthquakeModel, service: EarthquakeService = Depends()):
    try:
        result = service.process_earthquake_data(query)
        return result
    except ValueError as e:  # Captura erros conhecidos e retorna erros HTTP específicos
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:  # Captura erros inesperados
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
