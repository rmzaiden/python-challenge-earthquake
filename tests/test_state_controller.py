from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_add_state_success():
    """
    Scenario: Add a new state successfully
    """

    # Arrange
    state_data = {
        "name": "New State",
        "state_abbreviation": "NS",
        "country_id": 1
    }
    expected_response = {
        "id": 1,
        "name": "New State",
        "state_abbreviation": "NS",
        "country_id": 1
    }

    with patch('services.state_service.StateService.create_state', return_value=expected_response) as mock_create_state:
        
        # Act
        response = client.post("/v1/states/", json=state_data)

        # Assert
        assert response.status_code == 201
        assert response.json() == expected_response
        mock_create_state.assert_called_once()

def test_add_state_validation_error():
    """
    Scenario: Add a new state with invalid data
    """

    # Arrange
    state_data = {
        "name": "",
        "state_abbreviation": "NS",
        "country_id": 1
    }

    # Act
    response = client.post("/v1/states/", json=state_data)

    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()

def test_add_state_unexpected_error():
    """
    Scenario: An unexpected error occurs when adding a new state
    """

    # Arrange
    state_data = {
        "name": "New State",
        "state_abbreviation": "NS",
        "country_id": 1
    }

    with patch('services.state_service.StateService.create_state', side_effect=Exception("Unexpected Error")) as mock_create_state:
        
        # Act
        response = client.post("/v1/states/", json=state_data)

        # Assert
        assert response.status_code == 500
        assert response.json().get("detail") == "An unexpected error occurred"
        mock_create_state.assert_called_once()
