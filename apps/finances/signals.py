from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.sales.models import Sale
from apps.suppliers.models import SupplierTransaction

from .services import month_start, recalculate_month


@receiver(post_save, sender=Sale)
def update_budget_from_sale(sender, instance, **kwargs):
    recalculate_month(instance.sale_date)


@receiver(post_save, sender=SupplierTransaction)
def update_budget_from_supplier_tx(sender, instance, **kwargs):
    recalculate_month(instance.transacted_at.date())

