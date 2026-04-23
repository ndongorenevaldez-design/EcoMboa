import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import User
from apps.collection_points.models import CollectionPoint
from apps.finances.models import ImpactIndicator, MonthlyBudget
from apps.missions.models import Mission
from apps.notifications.models import Notification
from apps.reports.models import WasteReport
from apps.sales.models import Sale
from apps.sorting_center.models import SortingCenter
from apps.suppliers.models import SupplierTransaction

from .forms import AdminPortalLoginForm


def admin_portal_login(request):
    if request.user.is_authenticated and getattr(request.user, "role", "") == "admin":
        return redirect("dashboard:index")

    if request.method == "POST":
        form = AdminPortalLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            user = User.objects.filter(email__iexact=email, role="admin", is_active=True).first()
            if user and user.check_password(password):
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return redirect("dashboard:index")
            messages.error(request, "Invalid admin credentials.")
    else:
        form = AdminPortalLoginForm(initial={"email": "admin@gmail.com"})
    return render(request, "dashboard/admin_portal_login.html", {"form": form})


@login_required
def admin_portal_logout(request):
    logout(request)
    return redirect("dashboard:portal_login")


@login_required
def admin_dashboard(request):
    if getattr(request.user, "role", "") != "admin":
        return redirect("dashboard:portal_login")

    latest_budget = MonthlyBudget.objects.order_by("-month").first()
    latest_impact = ImpactIndicator.objects.order_by("-month").first()
    activity = []

    recent_reports = WasteReport.objects.order_by("-created_at")[:5]
    recent_missions = Mission.objects.order_by("-assigned_at")[:5]
    recent_transactions = SupplierTransaction.objects.order_by("-transacted_at")[:5]
    recent_sales = Sale.objects.order_by("-created_at")[:5]

    for item in recent_reports:
        activity.append({"when": item.created_at, "text": f"Report #{item.pk} submitted in {item.district}"})
    for item in recent_missions:
        activity.append({"when": item.assigned_at, "text": f"Mission #{item.pk} is {item.get_status_display().lower()}"})
    for item in recent_transactions:
        activity.append({"when": item.transacted_at, "text": f"Supplier transaction #{item.pk} recorded"})
    for item in recent_sales:
        activity.append({"when": item.created_at, "text": f"Sale #{item.pk} created for {item.buyer.company_name}"})
    activity.sort(key=lambda x: x["when"], reverse=True)

    map_items = []
    for point in CollectionPoint.objects.filter(status="active")[:80]:
        map_items.append(
            {
                "type": "point",
                "label": point.name,
                "lat": float(point.latitude),
                "lng": float(point.longitude),
            }
        )
    for center in SortingCenter.objects.filter(is_active=True):
        if center.latitude is not None and center.longitude is not None:
            map_items.append(
                {
                    "type": "center",
                    "label": center.name,
                    "lat": float(center.latitude),
                    "lng": float(center.longitude),
                }
            )

    chart_payload = {
        "budget": [
            {
                "month": item.month.strftime("%Y-%m"),
                "revenue": float(item.total_revenue),
                "balance": float(item.net_balance),
            }
            for item in reversed(list(MonthlyBudget.objects.order_by("-month")[:12]))
        ],
        "impact": [
            {
                "month": item.month.strftime("%Y-%m"),
                "collected": float(item.total_waste_collected_kg),
                "co2": float(item.co2_avoided_kg),
            }
            for item in reversed(list(ImpactIndicator.objects.order_by("-month")[:12]))
        ],
    }

    context = {
        "portal_links": [
            ("Reports", "/admin-eco/reports/"),
            ("Collection Points", "/admin-eco/collection-points/"),
            ("Suppliers", "/admin-eco/suppliers/approvals/"),
            ("Finances", "/admin-eco/finances/"),
            ("Sorting Center", "/center/"),
            ("Sales", "/center/sales/"),
            ("Partner Contracts", "/admin-eco/partners/contracts/"),
        ],
        "latest_budget": latest_budget,
        "latest_impact": latest_impact,
        "counts": {
            "reports": WasteReport.objects.count(),
            "missions": Mission.objects.count(),
            "sales": Sale.objects.count(),
            "notifications": Notification.objects.count(),
        },
        "activity": activity[:10],
        "map_items_json": json.dumps(map_items),
        "chart_payload_json": json.dumps(chart_payload),
    }
    return render(request, "dashboard/admin_dashboard.html", context)
