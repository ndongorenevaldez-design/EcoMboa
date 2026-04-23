from django.db import models


class SortingCenter(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MaterialStock(models.Model):
    MATERIAL_CATEGORIES = [
        ("plastic", "Plastic"),
        ("metal", "Metal"),
        ("paper", "Paper"),
        ("glass", "Glass"),
        ("organic", "Organic"),
        ("textile", "Textile"),
        ("ewaste", "E-Waste"),
    ]
    QUALITY_GRADES = [("A", "Grade A"), ("B", "Grade B"), ("C", "Grade C")]

    sorting_center = models.ForeignKey(
        SortingCenter, on_delete=models.CASCADE, related_name="material_stocks"
    )
    material_category = models.CharField(max_length=20, choices=MATERIAL_CATEGORIES)
    quality_grade = models.CharField(max_length=1, choices=QUALITY_GRADES)
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    low_stock_threshold_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("sorting_center", "material_category", "quality_grade")

    def __str__(self):
        return (
            f"{self.sorting_center} - {self.material_category} "
            f"{self.quality_grade} ({self.quantity_kg}kg)"
        )


class DeliveryReception(models.Model):
    MATERIAL_CATEGORIES = MaterialStock.MATERIAL_CATEGORIES
    QUALITY_GRADES = MaterialStock.QUALITY_GRADES

    sorting_center = models.ForeignKey(
        SortingCenter, on_delete=models.CASCADE, related_name="receptions"
    )
    mission = models.ForeignKey(
        "missions.Mission",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="receptions",
    )
    supplier_transaction = models.ForeignKey(
        "suppliers.SupplierTransaction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="receptions",
    )
    received_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delivery_receptions",
    )
    received_weight_kg = models.DecimalField(max_digits=12, decimal_places=2)
    material_category = models.CharField(max_length=20, choices=MATERIAL_CATEGORIES)
    quality_grade = models.CharField(max_length=1, choices=QUALITY_GRADES)
    confirmation_photo = models.ImageField(upload_to="sorting_center/receptions/", blank=True)
    lot_qr_code = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reception #{self.pk} - {self.sorting_center}"
