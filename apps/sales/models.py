from django.conf import settings
from django.db import models


class Sale(models.Model):
    STATUSES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    buyer = models.ForeignKey("buyers.BuyerProfile", on_delete=models.PROTECT, related_name="sales")
    sorting_center = models.ForeignKey(
        "sorting_center.SortingCenter", on_delete=models.PROTECT, related_name="sales"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_sales"
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="draft")
    sale_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    invoice_pdf = models.FileField(upload_to="sales/invoices/", blank=True)
    recycling_certificate_pdf = models.FileField(
        upload_to="sales/certificates/", blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sale #{self.pk}"


class SaleLine(models.Model):
    QUALITY_GRADES = [("A", "Grade A"), ("B", "Grade B"), ("C", "Grade C")]
    MATERIAL_CATEGORIES = [
        ("plastic", "Plastic"),
        ("metal", "Metal"),
        ("paper", "Paper"),
        ("glass", "Glass"),
        ("organic", "Organic"),
        ("textile", "Textile"),
        ("ewaste", "E-Waste"),
    ]

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lines")
    material_category = models.CharField(max_length=20, choices=MATERIAL_CATEGORIES)
    quality_grade = models.CharField(max_length=1, choices=QUALITY_GRADES)
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"SaleLine #{self.pk} ({self.material_category})"

