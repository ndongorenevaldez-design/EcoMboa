import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from apps.accounts.access import role_required
from apps.missions.models import Mission
from apps.suppliers.models import SupplierTransaction

from .forms import DeliveryReceptionForm, MaterialStockForm
from .models import DeliveryReception, MaterialStock, SortingCenter


@login_required
@role_required("center", "admin")
def center_dashboard(request):
    centers = SortingCenter.objects.filter(is_active=True).order_by("name")
    stocks = MaterialStock.objects.select_related("sorting_center").order_by(
        "sorting_center__name", "material_category", "quality_grade"
    )
    chart_data = list(
        stocks.values("material_category").annotate(total=Sum("quantity_kg")).order_by("material_category")
    )
    return render(
        request,
        "sorting_center/dashboard.html",
        {"centers": centers, "stocks": stocks, "chart_data_json": json.dumps(chart_data, default=float)},
    )


@login_required
@role_required("center", "admin")
def delivery_reception_create(request):
    if request.method == "POST":
        form = DeliveryReceptionForm(request.POST, request.FILES)
        if form.is_valid():
            reception = form.save(commit=False)
            reception.received_by = request.user
            if reception.lot_qr_code and not reception.mission_id and not reception.supplier_transaction_id:
                reception.mission = Mission.objects.filter(lot_qr_code=reception.lot_qr_code).first()
                reception.supplier_transaction = SupplierTransaction.objects.filter(
                    lot_qr_code=reception.lot_qr_code
                ).first()
            if not reception.lot_qr_code:
                reception.lot_qr_code = (
                    reception.mission.lot_qr_code
                    if reception.mission_id and reception.mission and reception.mission.lot_qr_code
                    else (
                        reception.supplier_transaction.lot_qr_code
                        if reception.supplier_transaction_id
                        and reception.supplier_transaction
                        and reception.supplier_transaction.lot_qr_code
                        else ""
                    )
                )
            reception.save()
            messages.success(request, "Delivery reception recorded and stock updated.")
            return redirect("sorting_center:index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = DeliveryReceptionForm()
    return render(request, "sorting_center/reception_form.html", {"form": form})


@login_required
@role_required("center", "admin")
def stock_edit(request):
    if request.method == "POST":
        form = MaterialStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock record saved.")
            return redirect("sorting_center:index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = MaterialStockForm()
    return render(request, "sorting_center/stock_form.html", {"form": form})


@login_required
@role_required("center", "admin")
def reception_history(request):
    receptions = DeliveryReception.objects.select_related(
        "sorting_center", "mission", "supplier_transaction", "received_by"
    ).order_by("-received_at")
    return render(request, "sorting_center/reception_history.html", {"receptions": receptions})

