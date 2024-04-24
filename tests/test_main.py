import json
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_notfoud_earthquakes_routers():
    """
    Scenario: The user tries to get the earthquakes information providing a city name, a start date and an end date and returns no results.
    """
    response = client.get(
        "/v1/earthquakes/",
        params={
            "city_name": "Los Angeles, CA",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "No results found."}


def test_get_foud_earthquakes_routers():
    """
    Scenario: The user tries to get the earthquakes information providing a city name, a start date and an end date and returns the closest earthquake to the city.
    """
    response = client.get(
        "/v1/earthquakes/",
        params={
            "city_name": "Los Angeles, CA",
            "start_date": "2024-01-01",
            "end_date": "2024-05-01",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "The closest earthquake to Los Angeles, CA was an M 5 - México on January 24"
    }

def test_set_invalid_start_date_earthquakes_routers():
    """
    Scenario: The user tries to get the earthquakes information providing a city name, a invalid start date and a valid end date and returns validation error message.
    """
    response = client.get(
        "/v1/earthquakes/",
        params={
            "city_name": "Los Angeles, CA",
            "start_date": "2024-011-01",
            "end_date": "2024-05-01",
        },
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail":"1 validation error for EarthquakeModel\nstart_date\n  Input should be a valid date or datetime, invalid date separator, expected `-` [type=date_from_datetime_parsing, input_value='2024-011-01', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.7/v/date_from_datetime_parsing"}

def test_set_invalid_end_date_earthquakes_routers():
    """
    Scenario: The user tries to get the earthquakes information providing a city name, a valid start date and an invalid end date and returns validation error message.
    """
    response = client.get(
        "/v1/earthquakes/",
        params={
            "city_name": "Los Angeles, CA",
            "start_date": "2024-01-01",
            "end_date": "2024-011-01",
        },
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail":"1 validation error for EarthquakeModel\nend_date\n  Input should be a valid date or datetime, invalid date separator, expected `-` [type=date_from_datetime_parsing, input_value='2024-011-01', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.7/v/date_from_datetime_parsing"}

@patch("controllers.city_controller.create_city")
def test_add_city_success(mock_create_city):
    mock_create_city.return_value = {
        "id": 1,
        "name": "Los Angeles",
        "state_province_id": 1,
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }

    city_data = {
        "name": "Los Angeles",
        "state_province_id": 1,
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    response = client.post("/v1/cities/", json=city_data)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Los Angeles"}


@patch("controllers.city_controller.create_city")
def test_add_city_success(mock_create_city):
    mock_create_city.return_value = {
        "id": 1,
        "name": "Los Angeles",
        "state_province_id": 1,
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }

    city_data = {
        "name": "Los Angeles",
        "state_province_id": 1,
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    response = client.post("/v1/cities/", json=city_data)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Los Angeles"}


@patch("controllers.city_controller.create_city")
def test_add_city_with_invalid_state_province(mock_create_city):

    mock_create_city.return_value = ""

    city_data = {
        "name": "Los Angeles",
        "state_province_id": "a",
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    response = client.post("/v1/cities/", json=city_data)
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "state_province_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "a",
            }
        ]
    }


@patch("controllers.city_controller.create_city")
def test_add_city_with_invalid_state_country(mock_create_city):

    mock_create_city.return_value = ""

    city_data = {
        "name": "Los Angeles",
        "state_province_id": 0,
        "country_id": "a",
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    response = client.post("/v1/cities/", json=city_data)
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "country_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "a",
            }
        ]
    }


@patch("controllers.city_controller.create_city")
def test_add_city_with_invalid_city_name(mock_create_city):

    mock_create_city.return_value = ""

    city_data = {
        "name": 1,
        "state_province_id": 0,
        "country_id": 1,
        "latitude": 40.7128,
        "longitude": -74.0060,
    }
    response = client.post("/v1/cities/", json=city_data)
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": 1,
                "loc": ["body", "name"],
                "msg": "Input should be a valid string",
                "type": "string_type",
            }
        ]
    }
