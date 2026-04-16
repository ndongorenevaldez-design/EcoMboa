from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('citizen', 'Citizen'),
        ('seller', 'Independent Seller'),
        ('collector', 'EcoMboa Collector'),
        ('center', 'Sorting Center'),
        ('buyer', 'Industrial Buyer'),
        ('partner', 'Partner Company'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    mobile_money_number = models.CharField(
        max_length=15, blank=True,
        help_text="MTN MoMo or Orange Money number"
    )
    mobile_money_operator = models.CharField(
        max_length=10, blank=True,
        choices=[('mtn', 'MTN MoMo'), ('orange', 'Orange Money')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
