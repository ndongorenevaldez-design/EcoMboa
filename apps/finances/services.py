from collections import OrderedDict
from datetime import date
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from openpyxl import Workbook

from apps.reports.models import WasteReport
from apps.sales.models import Sale
from apps.suppliers.models import SupplierTransaction

from .models import ImpactIndicator, MonthlyBudget


def month_start(value):
    return date(value.year, value.month, 1)


def recalculate_month(month):
    month = month_start(month)
    sales = Sale.objects.filter(sale_date__year=month.year, sale_date__month=month.month)
    supplier_txs = SupplierTransaction.objects.filter(
        transacted_at__year=month.year, transacted_at__month=month.month
    )
    reports = WasteReport.objects.filter(created_at__year=month.year, created_at__month=month.month)

    revenue = sum((sale.total_amount for sale in sales), Decimal("0.00"))
    payouts = sum((tx.total_amount for tx in supplier_txs), Decimal("0.00"))
    operational_costs = Decimal("0.00")
    gross_margin = revenue - payouts
    net_balance = gross_margin - operational_costs

    budget, _ = MonthlyBudget.objects.update_or_create(
        month=month,
        defaults={
            "total_revenue": revenue,
            "supplier_payouts": payouts,
            "operational_costs": operational_costs,
            "gross_margin": gross_margin,
            "net_balance": net_balance,
        },
    )

    total_collected = sum(
        (Decimal(str(report.estimated_quantity_kg)) for report in reports),
        Decimal("0.00"),
    )
    total_recycled = total_collected
    co2_avoided = total_recycled * Decimal("1.2")

    ImpactIndicator.objects.update_or_create(
        month=month,
        defaults={
            "total_waste_collected_kg": total_collected,
            "total_waste_recycled_kg": total_recycled,
            "co2_avoided_kg": co2_avoided,
            "active_citizens": reports.values("citizen_id").distinct().count(),
            "active_collectors": supplier_txs.values("collected_by_id").distinct().count(),
            "active_suppliers": supplier_txs.values("supplier_id").distinct().count(),
        },
    )
    return budget


def budget_series(limit=12):
    rows = MonthlyBudget.objects.order_by("-month")[:limit]
    ordered = list(reversed(rows))
    return [
        {
            "month": item.month.strftime("%Y-%m"),
            "revenue": float(item.total_revenue),
            "payouts": float(item.supplier_payouts),
            "balance": float(item.net_balance),
        }
        for item in ordered
    ]


def export_budget_workbook():
    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly Budgets"
    ws.append(["Month", "Revenue", "Supplier Payouts", "Operational Costs", "Gross Margin", "Net Balance"])
    for item in MonthlyBudget.objects.order_by("month"):
        ws.append(
            [
                item.month.strftime("%Y-%m"),
                float(item.total_revenue),
                float(item.supplier_payouts),
                float(item.operational_costs),
                float(item.gross_margin),
                float(item.net_balance),
            ]
        )
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()

