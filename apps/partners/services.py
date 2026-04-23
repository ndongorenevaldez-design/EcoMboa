from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_csr_certificate(report):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"CSR Certificate #{report.pk}")
    y = 800
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "EcoMboa CSR Certificate")
    y -= 36
    pdf.setFont("Helvetica", 11)
    lines = [
        f"Partner: {report.partner.company_name}",
        f"Period: {report.reporting_period_start} to {report.reporting_period_end}",
        f"Total collected: {report.total_collected_kg} kg",
        f"CO2 avoided: {report.co2_avoided_kg} kg",
        "EcoMboa certifies the above environmental contribution.",
    ]
    for line in lines:
        pdf.drawString(50, y, str(line))
        y -= 18
    pdf.save()
    report.certificate_pdf.save(
        f"csr_certificate_{report.pk}.pdf",
        ContentFile(buffer.getvalue()),
        save=False,
    )

