from fastapi import APIRouter
from app.services.ml_service import predict_disease

router = APIRouter()

@router.post("/predict-disease")
def disease_prediction(data: dict):

    symptoms = data.get("symptoms", "")

    prediction = predict_disease(symptoms)

    return {
        "input_symptoms": symptoms,
        "predicted_disease": prediction
    }