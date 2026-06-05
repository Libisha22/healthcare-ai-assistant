from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/chat")
async def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful healthcare assistant. "
                    "Provide educational information about health topics. "
                    "Do not diagnose diseases. "
                    "Encourage users to consult healthcare professionals "
                    "for medical advice, diagnosis, or treatment."
                )
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }