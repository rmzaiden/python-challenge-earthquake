from fastapi import APIRouter, Depends, HTTPException
from models.earthquake_model import EarthquakeModel
from services.earthquake_service import EarthquakeService

router = APIRouter()

@router.get("/earthquake/", response_model=str)
async def get_closest_earthquake(query: EarthquakeModel, service: EarthquakeService = Depends()):
    """
    Retrieves the closest earthquake based on the given query parameters.

    Args:
        query (EarthquakeModel): The query parameters for retrieving the closest earthquake.
        service (EarthquakeService, optional): The EarthquakeService instance used for processing the earthquake data. Defaults to Depends().

    Returns:
        The closest earthquake based on the given query parameters.

    Raises:
        HTTPException: If a known error occurs, an HTTPException with the appropriate status code and error message is raised.
    """
    try:
        result = service.process_earthquake_data(query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from exc
