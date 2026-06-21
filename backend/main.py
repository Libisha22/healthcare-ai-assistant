from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.symptoms import router as symptom_router
from app.routers.prediction import router as prediction_router
from app.routers.analytics import router as analytics_router
from app.routers.report import router as report_router

app = FastAPI(
    title="AI Healthcare Assistant",
    description="""
AI-powered healthcare assistant that:

• Analyzes symptoms using NLP

• Predicts diseases using Machine Learning

• Stores symptom history in PostgreSQL

• Provides confidence scores and recommendations
""",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(health_router)
app.include_router(symptom_router)
app.include_router(prediction_router)
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(report_router)

# Home Route
@app.get("/")
def home():
    return {
        "message": "Healthcare AI Assistant API Running"
    }