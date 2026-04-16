from django.conf import settings
from django.db import models


class BuyerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_profile"
    )
    company_name = models.CharField(max_length=180)
    trade_register_number = models.CharField(max_length=100, unique=True)
    desired_materials = models.JSONField(default=list, blank=True)
    monthly_capacity_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

