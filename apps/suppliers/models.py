from django.conf import settings
from django.db import models


class SupplierProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supplier_profile"
    )
    business_name = models.CharField(max_length=150, blank=True)
    national_id_number = models.CharField(max_length=80, blank=True)
    preferred_mobile_money_operator = models.CharField(
        max_length=10,
        choices=[("mtn", "MTN MoMo"), ("orange", "Orange Money")],
        blank=True,
    )
    preferred_mobile_money_number = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name or self.user.get_username()


class SupplierTransaction(models.Model):
    MATERIAL_TYPES = [
        ("plastic", "Plastic"),
        ("metal", "Metal"),
        ("paper", "Paper"),
        ("glass", "Glass"),
        ("organic", "Organic"),
        ("textile", "Textile"),
        ("ewaste", "E-Waste"),
    ]
    PAYMENT_STATUSES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    supplier = models.ForeignKey(
        SupplierProfile, on_delete=models.CASCADE, related_name="transactions"
    )
    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_supplier_transactions",
    )
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    mobile_money_operator = models.CharField(
        max_length=10, choices=[("mtn", "MTN MoMo"), ("orange", "Orange Money")]
    )
    mobile_money_number = models.CharField(max_length=20)
    mobile_money_reference = models.CharField(max_length=120, blank=True)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUSES, default="pending"
    )
    lot_qr_code = models.CharField(max_length=120, blank=True, unique=True, null=True)
    qr_code_image = models.ImageField(upload_to="suppliers/qr_codes/", blank=True)
    transacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SupplierTransaction #{self.pk} - {self.material_type}"
