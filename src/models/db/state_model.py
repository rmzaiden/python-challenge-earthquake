from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from helper.database import Base


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    __table_args__ = (UniqueConstraint("name", "country_id", name="_state_country_uc"),)
