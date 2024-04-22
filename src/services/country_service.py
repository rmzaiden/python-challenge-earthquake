import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helper.database import session_scope
from models.db.country_model import Country
from models.schemas.country_schema import CountryCreate


def create_country(country_create: CountryCreate) -> Country:
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
            raise ValueError(
                f"Cannot create country due to integrity constraints. Error: {exc}"
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise ValueError(
                f"An unexpected error occurred while processing your request. Error: {exc}"
            ) from exc


def get_countries():
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
            raise ValueError(
                f"An unexpected error occurred while fetching countries. Error: {exc}"
            )
