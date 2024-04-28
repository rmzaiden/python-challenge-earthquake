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
    assert response.status_code == 422
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

def test_list_states():
    """
    Scenario: List all states
    """
    expected_states = [
        {"id": 1, "name": "São Paulo", "state_abbreviation":"SP", "country_id": 1},
        {"id": 2, "name": "California", "state_abbreviation":"CA", "country_id": 2}
    ]

    with patch("services.state_service.StateService.get_states") as mock_get_states:
        # Arrange
        mock_get_states.return_value = expected_states

        # Act
        response = client.get("/v1/states/")

        # Assert
        assert response.status_code == 200
        assert response.json() == expected_states
        mock_get_states.assert_called_once()