from fastapi import APIRouter, Depends, HTTPException, Query, Path
from services.earthquake_service import EarthquakeService
from services.city_service import CityService
from models.schemas.earthquake_schema import EarthquakeModel, EarthquakeResponse

earthquake_router = APIRouter()

@earthquake_router.get("/v1/earthquakes/{city_id}", response_model=EarthquakeResponse)
def get_closest_earthquake(
    city_id: int = Path(..., description="The ID of the city"),
    start_date: str = Query(..., description="The start date of the date range"),
    end_date: str = Query(..., description="The end date of the date range"),
    city_service: CityService = Depends(),
    earthquake_service: EarthquakeService = Depends(),
):
    """
    Get the closest earthquake to a given city within a specified date range.

    Args:
        city_id (int): The ID of the city.
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.
        city_service (CityService): The service for retrieving city information.
        earthquake_service (EarthquakeService): The service for processing earthquake data.

    Returns:
        EarthquakeResponse: The response containing the closest earthquake information.

    Raises:
        HTTPException: If the city is not found or if there is an internal server error.
    """
    try:
        city = city_service.get_city_by_id(city_id)
        if not city:
            raise HTTPException(status_code=404, detail="City not found")

        state_abbreviation = city.state.state_abbreviation if city.state else ""
        query = EarthquakeModel(city_name=city.name, state_abbreviation=state_abbreviation, start_date=start_date, end_date=end_date)

        
        result = earthquake_service.process_earthquake_data(query)
        return EarthquakeResponse(message=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
