from fastapi import APIRouter
from app.database import SessionLocal
from app.models.symptom_record import SymptomRecord

router = APIRouter()

@router.get("/analytics")
def analytics():

    db = SessionLocal()

    history = db.query(
        SymptomRecord
    ).all()

    total_predictions = len(history)

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for item in history:

        symptom = item.symptom.lower()

        if "dengue" in symptom or "heart" in symptom:
            high_risk += 1

        elif "covid" in symptom or "bronchitis" in symptom:
            medium_risk += 1

        else:
            low_risk += 1

    db.close()

    return {
        "total_predictions": total_predictions,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }