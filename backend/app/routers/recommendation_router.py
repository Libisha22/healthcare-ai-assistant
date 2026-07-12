from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.hospital import Hospital

router = APIRouter()


doctor_mapping = {
    "flu": "General Physician",
    "covid19": "Pulmonologist",
    "dengue": "Infectious Disease Specialist",
    "malaria": "Infectious Disease Specialist",
    "heart_disease": "Cardiologist",
    "asthma": "Pulmonologist",
    "diabetes": "Endocrinologist"
}


@router.get("/recommend-hospitals")
def recommend_hospitals(disease: str):

    db: Session = SessionLocal()

    speciality = doctor_mapping.get(
        disease.lower(),
        "General Physician"
    )

    hospitals = db.query(Hospital).filter(
        Hospital.speciality == speciality
    ).all()

    result = []

    for hospital in hospitals:
        result.append({
            "id": hospital.id,
            "name": hospital.name,
            "speciality": hospital.speciality,
            "address": hospital.address,
            "city": hospital.city,
            "phone": hospital.phone,
            "latitude": hospital.latitude,
            "longitude": hospital.longitude,
            "rating": hospital.rating
        })

    db.close()

    return result