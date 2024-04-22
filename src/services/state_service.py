import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helper.database import session_scope
from models.db.state_model import State
from models.schemas.state_schema import StateCreate


def create_state(state_create: StateCreate) -> State:
    """
    Creates a new state in the database.

    Args:
        state_create (StateCreate): The data required to create a new state.

    Returns:
        State: The newly created state.

    Raises:
        ValueError: If the specified country ID does not exist.
        ValueError: If an unexpected error occurs while processing the request.
    """
    with session_scope() as db:
        try:
            state = State(name=state_create.name, country_id=state_create.country_id)
            db.add(state)
            db.commit()
            db.refresh(state)
            return state
        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                f"Cannot create state. The specified country ID {state_create.country_id} does not exist."
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise ValueError(
                "An unexpected error occurred while processing your request."
            ) from exc


def get_states():
    """
    Retrieve all states from the database.

    Returns:
        List[State]: A list of State objects representing the states in the database.
    """
    with session_scope() as db:
        return db.query(State).all()
