from fastapi import APIRouter
from sqlalchemy.orm import Session
from math import radians, sin, cos, sqrt, atan2

from app.database import SessionLocal
from app.models.hospital import Hospital

router = APIRouter()


doctor_mapping = {
    "flu": "General Physician",
    "covid19": "Pulmonologist",
    "bronchitis": "Pulmonologist",
    "dengue": "Infectious Disease Specialist",
    "malaria": "Infectious Disease Specialist",
    "heart_disease": "Cardiologist",
    "asthma": "Pulmonologist",
    "diabetes": "Endocrinologist"
}


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(R * c, 2)


@router.get("/recommend-hospitals")
def recommend_hospitals(
    disease: str,
    user_lat: float,
    user_lng: float
):

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

        distance = calculate_distance(
            user_lat,
            user_lng,
            hospital.latitude,
            hospital.longitude
        )

        result.append({
            "id": hospital.id,
            "name": hospital.name,
            "speciality": hospital.speciality,
            "address": hospital.address,
            "city": hospital.city,
            "phone": hospital.phone,
            "latitude": hospital.latitude,
            "longitude": hospital.longitude,
            "rating": hospital.rating,
            "distance": distance
        })

    result.sort(key=lambda x: x["distance"])

    db.close()

    return result[:5]