from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.schemas.state_schema import StateCreate, StateResponse
from services.state_service import StateService

state_router = APIRouter()


def get_state_service():
    """
    Returns an instance of the StateService class.
    """
    return StateService()


@state_router.post(
    "/v1/states/", response_model=StateResponse, status_code=status.HTTP_201_CREATED
)
def add_state(
    state_create: StateCreate, state_service: StateService = Depends(get_state_service)
):
    """
    Adds a new state to the system.

    Args:
        state_create (StateCreate): The data required to create a new state.

    Returns:
        State: The newly created state.

    Raises:
        HTTPException: If there is an error creating the state.
    """
    try:
        state = state_service.create_state(state_create)
        return state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e #pragma: no cover
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        ) from e


@state_router.get("/v1/states/", response_model=List[StateResponse])
def list_states(state_service: StateService = Depends(get_state_service)):
    """
    Retrieve a list of states.

    Returns:
        List[StateResponse]: A list of state responses.

    Raises:
        HTTPException: If there is a validation error (status code 400) or an unexpected error occurs (status code 500).
    """
    try:
        states = state_service.get_states()
        return states
    except ValueError as e: #pragma: no cover
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e: #pragma: no cover
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred"
        ) from e
