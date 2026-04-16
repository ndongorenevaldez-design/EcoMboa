from django.db import models


class MonthlyBudget(models.Model):
    month = models.DateField(unique=True, help_text="Use first day of month.")
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    supplier_payouts = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    operational_costs = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    gross_margin = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Budget {self.month:%Y-%m}"


class ImpactIndicator(models.Model):
    month = models.DateField(unique=True, help_text="Use first day of month.")
    total_waste_collected_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_waste_recycled_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    co2_avoided_kg = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    active_citizens = models.PositiveIntegerField(default=0)
    active_collectors = models.PositiveIntegerField(default=0)
    active_suppliers = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Impact {self.month:%Y-%m}"

