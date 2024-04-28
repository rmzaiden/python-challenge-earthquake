from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from models.schemas.country_schema import CountryCreate, CountryResponse
from services.country_service import CountryService
from main import app

client = TestClient(app)


def test_add_country_endpoint():
    """
    Scenario: Add a new country
    """

    # Arrange
    country_data = {"name": "New Country"}
    expected_country = {"id": 1, "name": "New Country"}

    with patch("services.country_service.CountryService.create_country", return_value=CountryResponse(**expected_country)) as mock_create_country:
        
        # Act
        response = client.post("/v1/countries/", json=country_data)
        
        # Assert
        assert response.status_code == 201, "Status code should be 201"
        assert response.json() == expected_country, "Response should match expected response"

        mock_create_country.assert_called_once_with(CountryCreate(**country_data))

def test_add_country_validation_error():
    """
    Scenario: Add a new country with invalid name
    """

    # Arrange
    country_data = {
        "name": ""
    }

    # Act
    response = client.post("/v1/countries/", json=country_data)

    # Assert
    assert response.status_code == 422

    response_json = response.json()

    detail = response_json["detail"][0]

    assert detail["type"] == "value_error"
    assert detail["loc"] == ["body", "name"]
    assert detail["msg"] == "Value error, The country name must not be empty or just spaces."
    assert detail["input"] == ""

def test_add_country_unexpected_error():
    """
    Scenario: An unexpected error occurs when adding a new country
    """
    # Arrange
    country_data = {
        "name": "New Country"
    }

    with patch("services.country_service.CountryService.create_country", side_effect=Exception("Unexpected error")) as mock_create_country:
        
        # Act
        response = client.post("/v1/countries/", json=country_data)

        # Assert
        assert response.status_code == 500
        assert response.json() == {"detail": "An unexpected error occurred"}
        mock_create_country.assert_called_once_with(CountryCreate(**country_data))


def test_list_countries():
    """
    Scenario: List all countries
    """
    expected_countries = [
        {"id": 1, "name": "Country One"},
        {"id": 2, "name": "Country Two"}
    ]

    with patch("services.country_service.CountryService.get_countries") as mock_get_countries:
        # Arrange
        mock_get_countries.return_value = expected_countries

        # Act
        response = client.get("/v1/countries/")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected_countries
        mock_get_countries.assert_called_once()