from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from app.database import SessionLocal
from app.models.symptom_record import SymptomRecord
from app.services.doctor_service import (
    get_doctor_info,
    doctor_mapping
)

router = APIRouter()


@router.get("/download-report")
def download_report():
    db = SessionLocal()
    latest_record = (
        db.query(SymptomRecord)
        .order_by(SymptomRecord.created_at.desc())
        .first()
    )
    db.close()

    pdf_file = (
        f"medical_report_{latest_record.id}.pdf"
        if latest_record
        else "medical_report.pdf"
    )

    c = canvas.Canvas(pdf_file)

    # ==================================
    # HEADER
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 24)
    c.drawString(180, 800, "MedScope AI")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(130, 775, "AI Healthcare Prediction Report")

    c.setFillColor(colors.black)
    c.line(50, 755, 550, 755)

    # ==================================
    # NO RECORD FOUND
    # ==================================
    if not latest_record:
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, "No prediction records available.")
        c.save()
        return FileResponse(pdf_file, media_type="application/pdf", filename="MedScope_Report.pdf")

    # ==================================
    # REPORT DETAILS (TOP SECTION)
    # ==================================
    report_id = f"MS-{latest_record.id}"

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)

    c.drawString(50, 735, f"Report ID: {report_id}")
    c.drawString(350, 735, f"Generated: {latest_record.created_at.strftime('%d/%m/%Y %I:%M %p')}")

    # Adjust Y since we added report details at the top
    y = 690

    # ==================================
    # FETCH DISEASE DETAILS
    # ==================================
    details = get_doctor_info(latest_record.predicted_disease)

    description = details.get("description", "AI-generated disease prediction.")
    doctor = details.get("doctor", "General Physician")
    medicines = details.get("medicines", [])
    precautions = details.get("precautions", [])

    hospital = doctor_mapping.get(
        latest_record.predicted_disease.lower(),
        {}
    ).get("hospital", "General Hospital")

    urgency = doctor_mapping.get(
        latest_record.predicted_disease.lower(),
        {}
    ).get("urgency", "Normal")

    confidence = latest_record.confidence or 0
    severity = latest_record.severity or "Low"

    disease_name = (
        latest_record.predicted_disease
        .replace("_", " ")
        .title()
    )

    # ==================================
    # PATIENT SYMPTOMS
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Patient Symptoms")

    y -= 25
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(70, y, latest_record.symptom)
    y -= 45

    # ==================================
    # PREDICTION DETAILS
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Prediction Details")

    y -= 25
    c.setFillColor(colors.black)
    c.drawString(70, y, f"Disease: {disease_name}")

    y -= 25
    c.drawString(70, y, f"Confidence Score: {confidence:.2f}%")

    # Confidence Bar
    y -= 20
    c.setFillColor(colors.lightgrey)
    c.rect(70, y, 350, 15, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#2563EB"))
    bar_width = min((confidence / 100) * 350, 350)
    c.rect(70, y, bar_width, 15, fill=1, stroke=0)
    c.setFillColor(colors.black)

    y -= 35

    # Colored Severity
    if severity.lower() == "high":
        c.setFillColor(colors.red)
    elif severity.lower() == "medium":
        c.setFillColor(colors.orange)
    else:
        c.setFillColor(colors.green)

    c.drawString(70, y, f"Severity Level: {severity}")
    c.setFillColor(colors.black)

    y -= 45

    # ==================================
    # DESCRIPTION
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Description")

    y -= 25
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    text = c.beginText(70, y)
    text.textLines(description)
    c.drawText(text)
    y -= 50

    # ==================================
    # DOCTOR
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Recommended Doctor")

    y -= 25
    c.setFillColor(colors.black)
    c.drawString(70, y, doctor)

    y -= 20
    c.drawString(70, y, f"Hospital: {hospital}")

    y -= 20
    c.drawString(70, y, f"Urgency: {urgency}")

    y -= 45

    # ==================================
    # MEDICINES
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Medicines")

    y -= 25
    c.setFillColor(colors.black)
    for med in medicines:
        c.drawString(70, y, f"• {med}")
        y -= 20
    y -= 20

    # ==================================
    # PRECAUTIONS
    # ==================================
    c.setFillColor(colors.HexColor("#2563EB"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Precautions")

    y -= 25
    c.setFillColor(colors.black)
    for item in precautions:
        c.drawString(70, y, f"• {item}")
        y -= 20
    y -= 30

    # ==================================
    # FIXED FOOTER
    # ==================================
    c.line(50, 80, 550, 80)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        65,
        "Disclaimer: This report is AI-generated and should not replace professional medical advice."
    )
    c.drawRightString(
        550,
        50,
        "Generated by MedScope AI v1.0"
    )

    c.save()

    return FileResponse(pdf_file, media_type="application/pdf", filename="MedScope_Report.pdf")
