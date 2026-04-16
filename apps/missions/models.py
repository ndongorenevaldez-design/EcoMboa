from django.db import models
from apps.accounts.models import User
from apps.reports.models import WasteReport
from apps.collection_points.models import CollectionPoint

class Mission(models.Model):
    SOURCE_TYPES = [
        ('report', 'Citizen report'),
        ('drop_point', 'Free drop-off point'),
        ('scheduled', 'Scheduled round'),
    ]
    STATUSES = [
        ('assigned', 'Assigned'),
        ('en_route', 'En route'),
        ('on_site', 'On site'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered to center'),
        ('cancelled', 'Cancelled'),
    ]
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    report = models.ForeignKey(
        WasteReport, on_delete=models.SET_NULL, null=True, blank=True
    )
    collection_point = models.ForeignKey(
        CollectionPoint, on_delete=models.SET_NULL, null=True, blank=True
    )
    collector = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='missions'
    )
    destination_center = models.ForeignKey(
        'sorting_center.SortingCenter', on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(max_length=20, choices=STATUSES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    confirmation_photo = models.ImageField(upload_to='confirmations/', blank=True)
    collected_weight_kg = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    lot_qr_code = models.CharField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return f"Mission {self.id} - {self.get_source_type_display()} ({self.get_status_display()})"
