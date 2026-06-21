from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class SymptomRecord(Base):

    __tablename__ = "symptom_records"

    id = Column(Integer, primary_key=True, index=True)

    symptom = Column(String, nullable=False)

    predicted_disease = Column(String)

    severity = Column(String)

    confidence = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )