from fastapi import APIRouter
from pydantic import BaseModel

from app.services.email_service import send_report_email

router = APIRouter()


class EmailRequest(BaseModel):
    email: str
    pdf_path: str


@router.post("/send-report-email")
async def send_email(request: EmailRequest):

    await send_report_email(
        request.email,
        request.pdf_path
    )

    return {
        "message": "Report emailed successfully"
    }