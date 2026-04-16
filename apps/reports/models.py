from django.db import models
from apps.accounts.models import User

class WasteReport(models.Model):
    TYPES = [
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('mixed', 'Mixed'),
    ]
    STATUSES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'Collection in progress'),
        ('collected', 'Collected'),
        ('processed', 'Processed at sorting center'),
        ('cancelled', 'Cancelled'),
    ]
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    waste_type = models.CharField(max_length=20, choices=TYPES)
    description = models.TextField()
    photo = models.ImageField(upload_to='reports/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    text_address = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    estimated_quantity_kg = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    is_urgent = models.BooleanField(default=False)
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.id} - {self.get_waste_type_display()} ({self.get_status_display()})"
