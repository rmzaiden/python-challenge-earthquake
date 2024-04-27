from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from helper.database import session_scope
from models.db.city_model import City
import re

class CityService:
    """
    Service class for managing cities.
    """

    def create_city(self, city_create):
        """
        Creates a new city in the database.

        Args:
            city_create (CityCreate): The data required to create a new city.

        Returns:
            City: The newly created city object.

        Raises:
            ValueError: If there is an issue with the provided foreign keys or an unexpected error occurs.
        """
        with session_scope() as db:
            try:
                city = City(
                    name=city_create.name,
                    state_province_id=city_create.state_province_id,
                    country_id=city_create.country_id,
                    latitude=city_create.latitude,
                    longitude=city_create.longitude,
                )
                db.add(city)
                db.commit()
                db.refresh(city)
                return city
            except IntegrityError as exc:
                db.rollback()
                error_message = self.parse_integrity_error_message(str(exc))
                raise ValueError(
                    f"Cannot create city. There might be an issue with the provided foreign keys: {error_message}"
                ) from exc
            except SQLAlchemyError as exc:
                db.rollback()
                raise ValueError("An unexpected error occurred while processing your request.") from exc

    def get_cities(self):
            """
            Retrieves all cities from the database.

            Returns:
                list: A list of City objects representing all the cities in the database.

            Raises:
                ValueError: If an unexpected error occurs while fetching cities from the database.
            """
            with session_scope() as db:
                try:
                    return db.query(City).all()
                except SQLAlchemyError as exc:
                    raise ValueError(f"An unexpected error occurred while fetching cities. Error: {exc}") from exc

    def get_city_by_id(self, city_id):
        """
        Retrieve a city by its ID.

        Args:
            city_id (int): The ID of the city to retrieve.

        Returns:
            City or None: The city object if found, otherwise None.
        """
        with session_scope() as db:
            city = db.query(City).filter(City.id == city_id).first()
            return city if city else None

    @staticmethod
    def parse_integrity_error_message(error_message):
        """
        Parses the integrity error message and returns a user-friendly error message.

        Args:
            error_message (str): The integrity error message to be parsed.

        Returns:
            str: A user-friendly error message indicating the invalid reference or foreign key values.

        """
        pattern = r'constraint "FK__.*?"\.\s*The conflict occurred in database ".*?", table "dbo\.(.*?)", column \'(.*?)\''
        match = re.search(pattern, error_message, re.IGNORECASE | re.DOTALL)
        if match:
            table, column = match.groups()
            return f"Invalid reference in table '{table}' for column '{column}'. Please ensure the reference is correct."
        return "Invalid foreign key reference. Please check your foreign key values."
