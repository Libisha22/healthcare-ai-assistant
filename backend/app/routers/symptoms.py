from fastapi import APIRouter
from app.models.symptom import SymptomRequest
from app.models.symptom_record import SymptomRecord
from app.database import SessionLocal
from app.services.diagnosis_service import analyze_symptom

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
def symptom_history():

    db = SessionLocal()

    records = db.query(SymptomRecord).all()

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "symptom": record.symptom
        })

    db.close()

    return result