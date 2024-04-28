import re

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from helper.database import session_scope
from models.db.city_model import City
from models.schemas.city_schema import CityCreate
from utils.logger import Logger

logger = Logger(name="city_service")

class CityService:
    """
    Service class for managing cities.
    """
    
    def create_city(self, city_create: CityCreate):
        """
        Creates a new city in the database.

        Args:
            city_create (CityCreate): The data required to create a new city.

        Returns:
            City: The newly created city object.

        Raises:
            ValueError: If there is an issue with the provided foreign keys or an unexpected error occurs.
        """
        logger.info(f"Starging creating city: {city_create}")
        with session_scope() as db:
            try:
                city = City(
                    name=city_create.name,
                    state_province_id=city_create.state_province_id,
                )
                db.add(city)
                db.commit()
                db.refresh(city)
                logger.info(f"City: {city_create} created successfully.")
                return city
            except IntegrityError as exc:
                db.rollback()
                error_message = self.extract_error_message(str(exc))
                logger.error(f"City: {city_create} creation failed. Error: {error_message}")
                raise ValueError(f"Cannot create city: {error_message}") from exc
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
        fk_violation_pattern = re.compile(
            r"conflicted with the FOREIGN KEY constraint", re.IGNORECASE
        )

        if unique_violation_match := unique_violation_pattern.search(exc_message):
            return f"Already exists city with name: {unique_violation_match.group(1)}"
        elif fk_violation_pattern.search(exc_message):
            return "State does not exist. Please provide a valid state_province_id."
        else:
            return "Data validation error. Please check the input data."

    def get_cities(self):
        """
        Retrieves all cities from the database.

        Returns:
            list: A list of City objects representing all the cities in the database.

        Raises:
            ValueError: If an unexpected error occurs while fetching cities from the database.
        """
        logger.info("Starting fetching cities.")
        with session_scope() as db:
            try:
                cities = db.query(City).all()
                logger.info("Cities fetched successfully.")
                return cities
            except SQLAlchemyError as exc:
                logger.error(f"An unexpected error occurred while fetching cities. Error: {exc}")
                raise ValueError(
                    f"An unexpected error occurred while fetching cities. Error: {exc}"
                ) from exc

    def get_city_by_id(self, city_id):
        """
        Retrieve a city by its ID.

        Args:
            city_id (int): The ID of the city to retrieve.

        Returns:
            City or None: The city object if found, None otherwise.
        """
        logger.info(f"Starting fetching city by ID: {city_id}")
        with session_scope() as db:
            try:
                city = (
                    db.query(City)
                    .options(joinedload(City.state))
                    .filter(City.id == city_id)
                    .first()
                )
                if city is None:
                    logger.warning(f"No city found with ID {city_id} in database.")
                    raise ValueError(f"No city found with ID {city_id} in database.")
                
                logger.info("City fetched successfully.")
                return city
            except SQLAlchemyError as exc:
                    logger.error(f"An unexpected error occurred while fetching. Error: {exc}")
                    raise ValueError(
                        f"An unexpected error occurred while fetching cities. Error: {exc}"
                    ) from exc
