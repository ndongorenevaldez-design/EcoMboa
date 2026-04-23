from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.access import role_required
from apps.sorting_center.models import MaterialStock

from .forms import BuyerProfileForm
from .models import BuyerProfile


@login_required
@role_required("buyer")
def buyer_dashboard(request):
    profile = BuyerProfile.objects.filter(user=request.user).first()
    sales = []
    if profile:
        sales = profile.sales.select_related("sorting_center").order_by("-created_at")[:20]
    return render(request, "buyers/dashboard.html", {"profile": profile, "sales": sales})


@login_required
@role_required("buyer")
def buyer_profile_edit(request):
    profile = BuyerProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = BuyerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if profile.pk is None:
                profile.is_approved = False
            profile.save()
            messages.success(request, "Buyer profile saved.")
            return redirect("buyers:index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = BuyerProfileForm(instance=profile)
    return render(request, "buyers/profile_form.html", {"form": form, "profile": profile})


@login_required
@role_required("buyer", "admin", "center")
def material_catalog(request):
    stocks = (
        MaterialStock.objects.select_related("sorting_center")
        .values("material_category", "quality_grade", "sorting_center__name")
        .annotate(total_quantity=Sum("quantity_kg"), average_price=Avg("unit_price"))
        .order_by("material_category", "quality_grade")
    )
    return render(request, "buyers/catalog.html", {"stocks": stocks})
