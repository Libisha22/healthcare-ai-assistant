from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import SessionLocal
from app.models.symptom_record import SymptomRecord
from app.services.auth_dependency import get_current_user

router = APIRouter()


@router.get("/analytics")
def get_analytics(
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

    if not user:
        db.close()
        return {}

    user_id = user.id

    records = (
        db.query(SymptomRecord)
        .filter(SymptomRecord.user_id == user_id)
        .all()
    )

    total_predictions = len(records)

    disease_count = {}

    for record in records:

        disease = record.predicted_disease

        if disease:

            disease_count[disease] = (
                disease_count.get(disease, 0) + 1
            )

    top_disease = None

    if disease_count:

        top_disease = max(
            disease_count,
            key=disease_count.get
        )

    latest_prediction = None

    if records:

        latest_prediction = records[-1].predicted_disease

    db.close()

    return {
        "total_predictions": total_predictions,
        "top_disease": top_disease,
        "latest_prediction": latest_prediction
    }