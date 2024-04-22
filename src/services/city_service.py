import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helper.database import session_scope
from models.db.city_model import City
from models.schemas.city_schema import CityCreate


def create_city(city_create: CityCreate) -> City:
    """
    Creates a new city in the database.

    Args:
        city_create (CityCreate): The data required to create a new city.

    Returns:
        City: The newly created city.

    Raises:
        ValueError: If there is an issue with the provided foreign keys or an unexpected error occurs while processing the request.
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
            raise ValueError(
                f"Cannot create city. There might be an issue with the provided foreign keys. Error: {exc}"
            ) from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise ValueError(
                f"An unexpected error occurred while processing your request. Error: {exc}"
            ) from exc
