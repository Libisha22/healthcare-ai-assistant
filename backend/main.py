from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.hospital import Hospital
from app.models.symptom_record import SymptomRecord

from app.routers.health import router as health_router
from app.routers.symptoms import router as symptom_router
from app.routers.prediction import router as prediction_router
from app.routers.analytics import router as analytics_router
from app.routers.report import router as report_router
from app.routers.email_routers import router as email_router
from app.routers.auth_router import router as auth_router
from app.routers.hospital_router import router as hospital_router
from app.routers.recommendation_router import router as recommendation_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedScope AI",
    description="""
AI-powered healthcare assistant that:

• Analyzes symptoms using NLP
• Predicts diseases using Machine Learning
• Stores symptom history in PostgreSQL
• Recommends hospitals based on location
• Provides confidence scores and recommendations
""",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(symptom_router)
app.include_router(prediction_router)
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(report_router)
app.include_router(email_router)
app.include_router(auth_router)
app.include_router(hospital_router)
app.include_router(recommendation_router)

# Home Route
@app.get("/")
def home():
    return {
        "message": "MedScope AI API Running"
    }