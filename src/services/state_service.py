import re
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from helper.database import session_scope
from models.db.state_model import State
from models.schemas.state_schema import StateCreate

class StateService:
    """
    Service class for managing states.
    """

    def create_state(self, state_create: StateCreate) -> State:
        """
        Creates a new state in the database.

        Args:
            state_create (StateCreate): The data required to create a new state.

        Returns:
            State: The newly created state.

        Raises:
            ValueError: If the specified country ID does not exist or an unexpected error occurs.
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
                    f"Cannot create state. The specified country ID {state_create.country_id} does not exist: {exc}"
                ) from exc
            except SQLAlchemyError as exc:
                db.rollback()
                raise ValueError(
                    f"An unexpected error occurred while processing your request: {exc}"
                ) from exc

    def get_states(self):
        """
        Retrieve all states from the database.

        Returns:
            List[State]: A list of State objects representing the states in the database.

        Raises:
            ValueError: If an unexpected database error occurs.
        """
        with session_scope() as db:
            try:
                return db.query(State).all()
            except SQLAlchemyError as exc:
                raise ValueError(
                    f"An unexpected error occurred while fetching states. Error: {exc}"
                )
