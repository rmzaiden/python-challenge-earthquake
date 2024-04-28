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
                state = State(
                    name=state_create.name, country_id=state_create.country_id
                )
                db.add(state)
                db.commit()
                db.refresh(state)
                return state
            except IntegrityError as exc:
                db.rollback()
                error_message = self.extract_error_message(str(exc))
                raise ValueError(f"Cannot create state: {error_message}") from exc
            except SQLAlchemyError as exc:
                db.rollback()
                raise ValueError(
                    "An unexpected error occurred while processing your request."
                ) from exc
            
    @staticmethod
    def extract_error_message(exc_message):
        """
        Extracts the error message from the exception message.

        Args:
            exc_message (str): The exception message.

        Returns:
            str: The extracted error message.

        """
        unique_violation_pattern = re.compile(
            r"Violation of UNIQUE KEY constraint.*?The duplicate key value is \((.*?)\).",
            re.IGNORECASE,
        )
        fk_violation_pattern = re.compile(
            r"conflicted with the FOREIGN KEY constraint", re.IGNORECASE
        )

        if unique_violation_match := unique_violation_pattern.search(exc_message):
            return f"Already exists state with name: {unique_violation_match.group(1)}"
        elif fk_violation_pattern.search(exc_message):
            return "Country does not exist. Please provide a valid country_id."
        else:
            return "Data validation error. Please check the input data."

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
