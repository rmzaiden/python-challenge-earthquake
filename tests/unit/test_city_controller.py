from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from models.schemas.city_schema import CityCreate
from main import app

client = TestClient(app)

def test_add_city_success():
    """
    Scenario: Add a new city successfully
    """

    # Arrange
    city_data = {
        "name": "New City",
        "state_province_id": 1
    }
    expected_response = {
        "id": 1,
        "name": "New City",
        "state_province_id": 1
    }

    with patch("services.city_service.CityService.create_city") as mock_create_city:
        mock_create_city.return_value = expected_response

        # Act
        response = client.post("/v1/cities/", json=city_data)

        # Assert
        assert response.status_code == 201
        assert response.json() == expected_response
        mock_create_city.assert_called_once_with(CityCreate(**city_data))

def test_add_city_validation_error():
    """
    Scenario: Add a new city with invalid name
    """

    # Arrange
    city_data = {
        "name": "", 
        "state_province_id": 1
    }

    # Act
    response = client.post("/v1/cities/", json=city_data)

    # Assert
    assert response.status_code == 422

    response_json = response.json()

    detail = response_json["detail"][0]

    assert detail["type"] == "value_error"
    assert detail["loc"] == ["body", "name"]
    assert detail["msg"] == "Value error, The city name must not be empty or just spaces."
    assert detail["input"] == ""

def test_add_city_unexpected_error():
    """
    Scenario: An unexpected error occurs when adding a new city
    """
    # Arrange
    city_data = {
        "name": "New City",
        "state_province_id": 1
    }

    with patch("services.city_service.CityService.create_city", side_effect=Exception("Unexpected error")) as mock_create_city:
        
        # Act
        response = client.post("/v1/cities/", json=city_data)

        # Assert
        assert response.status_code == 500
        assert response.json() == {'detail': 'An unexpected error occurred.'}
        mock_create_city.assert_called_once_with(CityCreate(**city_data))


def test_list_cities():
    """
    Scenario: List all cities
    """
    expected_cities = [
        {"id": 1, "name": "City One", "state_province_id": 1},
        {"id": 2, "name": "City Two", "state_province_id": 2}
    ]

    with patch("services.city_service.CityService.get_cities") as mock_get_cities:
        # Arrange
        mock_get_cities.return_value = expected_cities

        # Act
        response = client.get("/v1/cities/")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected_cities
        mock_get_cities.assert_called_once()

def test_add_city_invalid_state_id():
    """
    Scenario: Add a new city with an invalid state_province_id
    """
    city_data = {
        "name": "Valid Name", 
        "state_province_id": 99999
    }

    with patch("services.city_service.CityService.create_city") as mock_create_city:
        
        # Arrange
        mock_create_city.side_effect = ValueError("Cannot create city: State does not exist. Please provide a valid state_province_id.")
        
        # Act
        response = client.post("/v1/cities/", json=city_data)

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Cannot create city: State does not exist. Please provide a valid state_province_id."}

        mock_create_city.assert_called_once()      
