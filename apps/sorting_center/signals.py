from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import Notification

from .models import DeliveryReception, MaterialStock


@receiver(post_save, sender=DeliveryReception)
def update_stock_from_reception(sender, instance, created, **kwargs):
    if not created:
        return

    stock, _ = MaterialStock.objects.get_or_create(
        sorting_center=instance.sorting_center,
        material_category=instance.material_category,
        quality_grade=instance.quality_grade,
        defaults={"quantity_kg": Decimal("0.00")},
    )
    stock.quantity_kg = Decimal(stock.quantity_kg) + Decimal(instance.received_weight_kg)
    stock.save()


@receiver(post_save, sender=MaterialStock)
def create_low_stock_alert(sender, instance, **kwargs):
    if instance.low_stock_threshold_kg and instance.quantity_kg <= instance.low_stock_threshold_kg:
        admins = get_user_model().objects.filter(role="admin", is_active=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                notification_type="stock",
                title="Low stock alert",
                message=(
                    f"{instance.sorting_center.name}: {instance.material_category} "
                    f"{instance.quality_grade} is at {instance.quantity_kg} kg."
                ),
                payload={
                    "sorting_center_id": instance.sorting_center_id,
                    "material_category": instance.material_category,
                    "quality_grade": instance.quality_grade,
                },
            )
