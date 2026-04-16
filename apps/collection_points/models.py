from django.db import models
from apps.accounts.models import User

class CollectionPoint(models.Model):
    TYPE_CHOICES = [
        ('paid', 'Paid Collection Point'),
        ('free', 'Free Drop-Off Point'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('full', 'Full — max capacity reached'),
    ]
    name = models.CharField(max_length=200)
    point_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    district = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_points'
    )
    
    # Accepted waste types
    accepts_plastic = models.BooleanField(default=True)
    accepts_metal = models.BooleanField(default=True)
    
    # Capacity and fill level
    capacity_kg_day = models.FloatField(default=500)
    current_stock_kg = models.FloatField(default=0)
    fill_level = models.IntegerField(default=0, help_text="Percentage 0-100")
    
    # Payment info (TYPE A only)
    plastic_price_kg = models.FloatField(null=True, blank=True, help_text="Purchase price FCFA/kg")
    metal_price_kg = models.FloatField(null=True, blank=True)
    
    # Opening hours (TYPE A only)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    opening_days = models.CharField(max_length=100, blank=True, help_text="e.g. Mon-Fri, Sat")
    
    # Meta
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    photo = models.ImageField(upload_to='collection_points/', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_point_type_display()})"
