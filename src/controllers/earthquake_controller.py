from fastapi import APIRouter, Depends, HTTPException, Query

from models.schemas.earthquake_schema import EarthquakeModel, EarthquakeResponse
from services.earthquake_service import EarthquakeService

router = APIRouter()


@router.get("/earthquake/", response_model=EarthquakeResponse)
def get_closest_earthquake(
    city_name: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    service: EarthquakeService = Depends(),
):
    """
    Retrieves the closest earthquake data for a given city within a specified date range.

    Args:
        city_name (str): The name of the city.
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.
        service (EarthquakeService): An instance of the EarthquakeService class.

    Returns:
        EarthquakeResponse: The response object containing the result message.

    Raises:
        HTTPException: If an error occurs during the processing of earthquake data.
    """
    try:
        query = EarthquakeModel(
            city_name=city_name, start_date=start_date, end_date=end_date
        )
        result = service.process_earthquake_data(query)
        return EarthquakeResponse(message=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
