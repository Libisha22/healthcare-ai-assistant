from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check"
)
def health_check():
    return {
        "status": "healthy",
        "service": "Healthcare AI Assistant"
    }