from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from helper.database import Base


class State(Base):
    """
    Represents a state in the database.

    Attributes:
        id (int): The unique identifier for the state.
        name (str): The name of the state.
        state_abbreviation (str): The abbreviation of the state.
        country_id (int): The foreign key referencing the country to which the state belongs.
        cities (relationship): The relationship to the cities associated with the state.
    """

    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state_abbreviation = Column(String(2), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    __table_args__ = (UniqueConstraint("name", "country_id", name="_state_country_uc"),)
    cities = relationship("City", back_populates="state")
