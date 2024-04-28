from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from models.schemas.earthquake_schema import EarthquakeModel

client = TestClient(app)


@patch("services.city_service.CityService.get_city_by_id")
@patch("services.earthquake_service.EarthquakeService.process_earthquake_data")
def test_get_closest_earthquake_success(mock_process_earthquake, mock_get_city_by_id):
    """
    Scenario: Successfully getting the closest earthquake to a city within a specified date range.
    """

    # Arrange
    mock_state = MagicMock()
    mock_state.state_abbreviation = "CA"

    mock_city = MagicMock()
    mock_city.id = 1
    mock_city.name = 'Los Angeles'
    mock_city.state = mock_state
    mock_get_city_by_id.return_value = mock_city

    expected_message = "Result for Los Angeles, CA between January 01, 2021 and July 07, 2021: The closest earthquake to Los Angeles was an M 5.25 - Severe Road, Fondo, Imperial County, California, United States on June 05"
    mock_process_earthquake.return_value = {"message": expected_message}

    # Act
    response = client.get("/v1/earthquakes/1?start_date=2021-01-01&end_date=2021-07-02")
    print(response.text)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}

    mock_get_city_by_id.assert_called_once_with(1)

    mock_process_earthquake.assert_called_once_with(
        EarthquakeModel(
            city_id=1,
            city_name="Los Angeles",
            state_abbreviation="CA",
            start_date="2021-01-01",
            end_date="2021-07-02",
        )
    )


@patch("services.city_service.CityService.get_city_by_id")
def test_get_closest_earthquake_city_not_found(mock_get_city_by_id):
    """
    Scenario: The city is not found.
    """

    # Arrange
    mock_get_city_by_id.return_value = None

    # Act
    response = client.get(
        "/v1/earthquakes/999?start_date=2021-01-01&end_date=2021-01-02"
    )

    # Assert
    assert (
        response.status_code == 404
    ), f"Expected 404 but got {response.status_code}. Response: {response.json()}"

    assert response.json() == {
        "detail": "City not found"
    }, "The error message for a not found city is incorrect."

    mock_get_city_by_id.assert_called_once_with(999)


@patch("services.city_service.CityService.get_city_by_id")
@patch("services.earthquake_service.EarthquakeService.process_earthquake_data")
def test_get_closest_earthquake_unexpected_error(
    mock_process_earthquake, mock_get_city_by_id
):
    """
    Scenario: An unexpected error occurs while processing the earthquake data.
    """

    # Arrange
    mock_city = MagicMock()
    mock_city.name = "Los Angeles"
    mock_city.state.state_abbreviation = "CA"
    mock_get_city_by_id.return_value = mock_city

    mock_process_earthquake.side_effect = Exception("Unexpected error")

    # Act
    response = client.get("/v1/earthquakes/1?start_date=2021-01-01&end_date=2021-01-02")

    # Assert
    assert (
        response.status_code == 500
    ), f"Expected status 500 but got {response.status_code}. Response: {response.json()}"
    assert response.json() == {
        "detail": "Unexpected error"
    }, "The error message in the response is incorrect."

    mock_get_city_by_id.assert_called_once_with(1)
    mock_process_earthquake.assert_called_once()