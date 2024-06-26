import re

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helper.database import session_scope
from models.db.country_model import Country
from utils.logger import Logger

logger = Logger(name="country_service")

class CountryService:
    """
    Service class for managing countries.
    """

    def create_country(self, country_create):
        """
        Creates a new country in the database.

        Args:
            country_create (CountryCreate): The data required to create a new country.

        Returns:
            Country: The newly created country.

        Raises:
            ValueError: If there is an issue with the database insertion.
        """
        logger.info(f"Starting creating country: {country_create}")
        with session_scope() as db:
            try:
                country = Country(name=country_create.name)
                db.add(country)
                db.commit()
                db.refresh(country)
                logger.info(f"Country: {country_create} created successfully.")
                return country
            except IntegrityError as exc:
                db.rollback()
                logger.error(f"Country: {country_create} creation failed. Error: {exc}")
                error_message = self.extract_error_message(str(exc))
                raise ValueError(f"Cannot create country: {error_message}") from exc
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
        logger.info(f"Extracting error message from: {exc_message}")
        unique_violation_pattern = re.compile(
            r"Violation of UNIQUE KEY constraint.*?The duplicate key value is \((.*?)\).",
            re.IGNORECASE,
        )

        if unique_violation_match := unique_violation_pattern.search(exc_message):
            return (
                f"Already exists country with name: {unique_violation_match.group(1)}"
            )
        else:
            return "Data validation error. Please check the input data."

    def get_countries(self):
        """
        Retrieve all countries from the database.

        Returns:
            List[Country]: A list of Country objects representing the countries in the database.

        Raises:
            ValueError: If an unexpected database error occurs.
        """
        logger.info("Starting fetching countries.")
        with session_scope() as db:
            try:
                return db.query(Country).all()
            except SQLAlchemyError as exc:
                logger.error(f"An unexpected error occurred while fetching countries. Error: {exc}")
                raise ValueError(
                    f"An unexpected error occurred while fetching countries. Error: {exc}"
                ) from exc
