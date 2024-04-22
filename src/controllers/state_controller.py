from typing import List

from fastapi import APIRouter, HTTPException

from models.schemas.state_schema import StateCreate, StateResponse
from services.state_service import create_state, get_states

state_router = APIRouter()


@state_router.post("/states/", response_model=StateResponse)
def add_state(state_create: StateCreate):
    try:
        return create_state(state_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@state_router.get("/states/", response_model=List[StateResponse])
def list_states():
    states = get_states()
    return states
