from django.db import models
from django.utils import timezone


class Notification(models.Model):
    TYPE_CHOICES = [
        ("system", "System"),
        ("report", "Report"),
        ("mission", "Mission"),
        ("payment", "Payment"),
        ("sale", "Sale"),
        ("stock", "Stock"),
        ("partner", "Partner"),
    ]

    recipient = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=160)
    message = models.TextField()
    payload = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=["is_read", "read_at"])

    def __str__(self):
        return f"{self.title} -> {self.recipient}"

