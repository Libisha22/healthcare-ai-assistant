from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    speciality = Column(String)

    address = Column(String)
    city = Column(String)

    phone = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    rating = Column(Float)