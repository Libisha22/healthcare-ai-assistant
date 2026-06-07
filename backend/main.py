from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.symptoms import router as symptom_router
from app.routers.prediction import router as prediction_router
app = FastAPI(
    title="Healthcare AI Assistant",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(symptom_router)
app.include_router(prediction_router)

@app.get("/")
def home():
    return {
        "message": "Healthcare AI Assistant API Running"
    }