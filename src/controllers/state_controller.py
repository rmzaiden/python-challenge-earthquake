from typing import List

from fastapi import APIRouter, HTTPException

from models.schemas.state_schema import StateCreate, StateResponse
from services.state_service import create_state, get_states

state_router = APIRouter()


@state_router.post("/states/", response_model=StateResponse)
def add_state(state_create: StateCreate):
    """
    Adds a new state to the system.

    Args:
        state_create (StateCreate): The state information to be created.

    Returns:
        State: The newly created state.

    Raises:
        HTTPException: If there is an error creating the state.
    """
    try:
        return create_state(state_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e


@state_router.get("/states/", response_model=List[StateResponse])
def list_states():
    """
    Retrieves a list of states.

    Returns:
        list: A list of states.
    """
    try:
        states = get_states()
        return states
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from e
