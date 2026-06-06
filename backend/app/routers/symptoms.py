from fastapi import APIRouter
from app.models.symptom import SymptomRequest
from app.services.diagnosis_service import analyze_symptom

router = APIRouter()

@router.post("/symptom-checker")
def symptom_checker(data: SymptomRequest):

    conditions = analyze_symptom(data.symptom)

    return {
        "symptom": data.symptom,
        "possible_conditions": conditions
    }