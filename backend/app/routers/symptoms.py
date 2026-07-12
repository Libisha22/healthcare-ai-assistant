from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.models.symptom import SymptomRequest
from app.models.symptom_record import SymptomRecord
from app.database import SessionLocal
from app.services.diagnosis_service import analyze_symptom
from app.services.auth_dependency import get_current_user

router = APIRouter()


@router.post("/symptom-checker")
def symptom_checker(data: SymptomRequest):

    db = SessionLocal()

    record = SymptomRecord(
        symptom=data.symptom
    )

    db.add(record)
    db.commit()

    conditions = analyze_symptom(data.symptom)

    db.close()

    return {
        "symptom": data.symptom,
        "possible_conditions": conditions
    }


@router.get("/symptom-history")
def symptom_history(
    current_user=Depends(get_current_user)
):

    db = SessionLocal()

    email = current_user["sub"]

    user = db.execute(
        text("""
            SELECT id
            FROM users
            WHERE email = :email
        """),
        {
            "email": email
        }
    ).fetchone()

    records = (
        db.query(SymptomRecord)
        .filter(SymptomRecord.user_id == user.id)
        .order_by(SymptomRecord.created_at.desc())
        .all()
    )

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "symptom": record.symptom,
            "predicted_disease": record.predicted_disease,
            "confidence": record.confidence,
            "severity": record.severity,
            "created_at": record.created_at
        })

    db.close()

    return result