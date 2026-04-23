from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.accounts.access import role_required

from .models import ImpactIndicator, MonthlyBudget
from .services import budget_series, export_budget_workbook, recalculate_month


@login_required
@role_required("admin")
def finance_dashboard(request):
    recalculate_month(date.today())
    budgets = MonthlyBudget.objects.order_by("-month")[:12]
    indicators = ImpactIndicator.objects.order_by("-month")[:12]
    return render(
        request,
        "finances/dashboard.html",
        {
            "budgets": budgets,
            "indicators": indicators,
            "series": budget_series(),
        },
    )


@login_required
@role_required("admin")
def export_budget_excel(request):
    payload = export_budget_workbook()
    response = HttpResponse(
        payload,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="monthly_budgets.xlsx"'
    return response

