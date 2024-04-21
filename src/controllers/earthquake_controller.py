from fastapi import APIRouter, Depends, HTTPException
from services.earthquake_service import EarthquakeService
from models.earthquake_model import EarthquakeModel
from models.response_models import EarthquakeResponse

router = APIRouter()

@router.get("/earthquake/", response_model=EarthquakeResponse)
def get_closest_earthquake(query: EarthquakeModel, service: EarthquakeService = Depends()):
    """
    Get the closest earthquake based on the given query parameters.

    Args:
        query (EarthquakeModel): The query parameters for the earthquake.
        service (EarthquakeService, optional): The EarthquakeService instance to use. Defaults to Depends().

    Returns:
        EarthquakeResponse: The response containing the closest earthquake information.

    Raises:
        HTTPException: If an error occurs while processing the earthquake data.
    """
    try:
        result = service.process_earthquake_data(query)
        return EarthquakeResponse(message=result['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))