from fastapi import Depends
from sqlalchemy import text
from app.services.auth_dependency import get_current_user



from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from app.services.ml_service import predict_disease
from app.services.doctor_service import get_doctor_info

from app.database import SessionLocal
from app.models.symptom_record import SymptomRecord

router = APIRouter()


# Request Model
class PredictionRequest(BaseModel):
    symptoms: str


# Disease Prediction Model
class DiseasePrediction(BaseModel):
    disease: str
    confidence: float
    description: Optional[str] = None
    severity: Optional[str] = None
    doctor: Optional[str] = None
    medicines: Optional[List[str]] = None
    precautions: Optional[List[str]] = None


# Response Model
class PredictionResponse(BaseModel):
    input_symptoms: str
    predictions: List[DiseasePrediction]


@router.post(
    "/predict-disease",
    summary="Predict Disease",
    description="Predicts possible diseases from symptoms using a trained Machine Learning model",
    response_model=PredictionResponse
)
def disease_prediction(
    data: PredictionRequest,
    current_user=Depends(get_current_user)
):
    # Run ML Model
    predictions = predict_disease(data.symptoms)

    # Add disease details
    for prediction in predictions:
        details = get_doctor_info(prediction["disease"])
        prediction["doctor"] = details.get("doctor")
        prediction["severity"] = details.get("severity")
        prediction["description"] = details.get("description")
        prediction["medicines"] = details.get("medicines")
        prediction["precautions"] = details.get("precautions")

    # Save Top Prediction to PostgreSQL
    try:
        if len(predictions) > 0:

            top_prediction = predictions[0]

            print("TOP PREDICTION =", top_prediction)

            db = SessionLocal()

            # Get logged-in user's email from JWT
            email = current_user["sub"]

            # Find user id from users table
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
                raise Exception("User not found")

            record = SymptomRecord(
                user_id=user.id,
                symptom=data.symptoms,
                predicted_disease=top_prediction.get("disease"),
                severity=top_prediction.get("severity"),
                confidence=float(top_prediction["confidence"])
            )

            db.add(record)
            db.commit()

            print("DATA SAVED SUCCESSFULLY")
            print("USER ID =", user.id)

            db.close()
    except Exception as e:
        print("DATABASE ERROR:", e)

    # Return Response
    return {
        "input_symptoms": data.symptoms,
        "predictions": predictions
    }
