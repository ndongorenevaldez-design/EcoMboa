from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def calculate_sale_totals(sale):
    total = Decimal("0.00")
    for line in sale.lines.all():
        line.line_total = Decimal(line.quantity_kg) * Decimal(line.unit_price)
        line.save(update_fields=["line_total"])
        total += line.line_total
    sale.total_amount = total
    sale.save(update_fields=["total_amount", "updated_at"])
    return total


def _build_pdf(title, lines):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(title)
    y = 800
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, title)
    y -= 32
    pdf.setFont("Helvetica", 11)
    for text in lines:
        pdf.drawString(50, y, str(text))
        y -= 18
        if y < 70:
            pdf.showPage()
            y = 800
            pdf.setFont("Helvetica", 11)
    pdf.save()
    return buffer.getvalue()


def generate_invoice_pdf(sale):
    payload = _build_pdf(
        f"EcoMboa Invoice #{sale.pk}",
        [
            f"Buyer: {sale.buyer.company_name}",
            f"Sorting center: {sale.sorting_center.name}",
            f"Status: {sale.get_status_display()}",
            f"Total amount: {sale.total_amount} FCFA",
            f"Due date: {sale.due_date or '-'}",
        ]
        + [
            f"{line.material_category} {line.quality_grade} - {line.quantity_kg} kg x {line.unit_price} = {line.line_total}"
            for line in sale.lines.all()
        ],
    )
    sale.invoice_pdf.save(f"invoice_{sale.pk}.pdf", ContentFile(payload), save=False)


def generate_certificate_pdf(sale):
    payload = _build_pdf(
        f"Recycling Certificate #{sale.pk}",
        [
            f"Buyer: {sale.buyer.company_name}",
            f"EcoMboa certifies delivery of recyclable materials.",
            f"Sorting center: {sale.sorting_center.name}",
            f"Total amount: {sale.total_amount} FCFA",
        ],
    )
    sale.recycling_certificate_pdf.save(
        f"certificate_{sale.pk}.pdf", ContentFile(payload), save=False
    )

