from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from helper.database import Base


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state_abbreviation = Column(String(2), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    __table_args__ = (UniqueConstraint("name", "country_id", name="_state_country_uc"),)
    cities = relationship("City", back_populates="state")
