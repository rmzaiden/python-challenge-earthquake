import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from helper.database import session_scope
from models.db.country_model import Country
from models.schemas.country_schema import CountryCreate


def create_country(country_create: CountryCreate) -> Country:
    with session_scope() as db:
        country = Country(name=country_create.name)
        db.add(country)
        db.commit()
        db.refresh(country)
        return country


def get_countries():
    with session_scope() as db:
        return db.query(Country).all()
