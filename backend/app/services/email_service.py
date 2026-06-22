from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_report_email(receiver_email: str, pdf_path: str):

    print("PDF PATH =", pdf_path)
    print("FILE EXISTS =", os.path.exists(pdf_path))
    message = MessageSchema(
        subject="MedScope AI Medical Report",
        recipients=[receiver_email],
        body="""
Hello,

Your MedScope AI Healthcare Report has been generated successfully.

Please find the attached PDF report.

This report is AI-generated and should not replace professional medical diagnosis.

Regards,
MedScope AI Team
        """,
        subtype="plain",

        attachments=[
            {
                "file": pdf_path
            }
        ]
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    print("EMAIL SENT SUCCESSFULLY")