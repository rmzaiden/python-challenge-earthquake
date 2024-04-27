import re
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from helper.database import session_scope
from models.db.country_model import Country

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
        with session_scope() as db:
            try:
                country = Country(name=country_create.name)
                db.add(country)
                db.commit()
                db.refresh(country)
                return country
            except IntegrityError as exc:
                db.rollback()
                error_message = self.extract_error_message(str(exc))
                raise ValueError(f"Cannot create country: {error_message}") from exc
            except SQLAlchemyError as exc:
                db.rollback()
                raise ValueError("An unexpected error occurred while processing your request.") from exc

    def get_countries(self):
        """
        Retrieve all countries from the database.

        Returns:
            List[Country]: A list of Country objects representing the countries in the database.

        Raises:
            ValueError: If an unexpected database error occurs.
        """
        with session_scope() as db:
            try:
                return db.query(Country).all()
            except SQLAlchemyError as exc:
                raise ValueError(f"An unexpected error occurred while fetching countries. Error: {exc}") from exc

    @staticmethod
    def extract_error_message(exc_message):
        """
        Extracts and returns a user-friendly error message from SQL exception messages.
        
        Args:
            exc_message (str): The exception message.

        Returns:
            str: A user-friendly error message.
        """
        unique_violation_pattern = re.compile(r"Violation of UNIQUE KEY constraint.*?The duplicate key value is \((.*?)\).", re.IGNORECASE)
        
        if unique_violation_match := unique_violation_pattern.search(exc_message):
            return f"Duplicate entry '{unique_violation_match.group(1)}' for unique column."
        else:
            return "Data validation error. Please check the input data."
