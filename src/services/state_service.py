import re

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helper.database import session_scope
from models.db.state_model import State
from models.schemas.state_schema import StateCreate
from utils.logger import Logger

logger = Logger(name="state_service")


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
        logger.info(f"Starting creating state: {state_create}")
        with session_scope() as db:
            try:
                state = State(
                    name=state_create.name, state_abbreviation=state_create.state_abbreviation, country_id=state_create.country_id
                )
                db.add(state)
                db.commit()
                db.refresh(state)
                logger.info(f"State: {state_create.name} created successfully.")
                return state
            except IntegrityError as exc:
                db.rollback()
                error_message = self.extract_error_message(str(exc))
                logger.error(f"State: {state_create.name} creation failed. Error: {exc}")
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
        logger.debug(f"Extracting error message from: {exc_message}")
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
        logger.info("Retrieving all states.")
        with session_scope() as db:
            try:
                return db.query(State).all()
            except SQLAlchemyError as exc:
                logger.error(f"An unexpected error occurred while fetching states. Error: {exc}")
                raise ValueError(f"An unexpected error occurred while fetching states. Error: {exc}") from exc
