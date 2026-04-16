from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.access import role_required

from .forms import SupplierProfileForm, SupplierTransactionForm
from .models import SupplierProfile, SupplierTransaction
from .services import generate_transaction_qr, simulate_mobile_money_payment


@login_required
@role_required("seller")
def supplier_dashboard(request):
    profile = SupplierProfile.objects.filter(user=request.user).first()
    transactions = []
    if profile:
        transactions = profile.transactions.select_related("collected_by").order_by("-transacted_at")[:20]
    return render(
        request,
        "suppliers/dashboard.html",
        {"profile": profile, "transactions": transactions},
    )


@login_required
@role_required("seller")
def supplier_profile_edit(request):
    profile = SupplierProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = SupplierProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if profile.pk is None:
                profile.is_approved = False
            profile.save()
            messages.success(request, "Supplier profile submitted successfully.")
            return redirect("suppliers:index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = SupplierProfileForm(instance=profile)
    return render(request, "suppliers/profile_form.html", {"form": form, "profile": profile})


@login_required
@role_required("seller")
def supplier_transaction_history(request):
    profile = get_object_or_404(SupplierProfile, user=request.user)
    transactions = profile.transactions.select_related("collected_by").order_by("-transacted_at")
    return render(request, "suppliers/transaction_history.html", {"transactions": transactions})


@login_required
@role_required("collector", "admin")
def supplier_transaction_create(request):
    if request.method == "POST":
        form = SupplierTransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                tx = form.save(commit=False)
                tx.collected_by = request.user
                tx.total_amount = form.cleaned_data["total_amount"]
                tx.payment_status = "pending"
                if form.cleaned_data.get("simulate_mobile_money", True):
                    status, ref = simulate_mobile_money_payment(
                        tx.mobile_money_operator, tx.total_amount
                    )
                    tx.payment_status = status
                    tx.mobile_money_reference = ref
                tx.save()
                generate_transaction_qr(tx)
                tx.save(update_fields=["lot_qr_code", "qr_code_image"])
            messages.success(request, "Supplier transaction recorded successfully.")
            return redirect("suppliers:collector_transactions")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = SupplierTransactionForm()
    return render(request, "suppliers/collector_transaction_form.html", {"form": form})


@login_required
@role_required("collector", "admin")
def collector_transaction_list(request):
    qs = SupplierTransaction.objects.select_related("supplier__user", "collected_by").order_by(
        "-transacted_at"
    )
    if request.user.role == "collector":
        qs = qs.filter(collected_by=request.user)
    return render(request, "suppliers/collector_transactions.html", {"transactions": qs[:120]})


@login_required
@role_required("admin")
def admin_supplier_approvals(request):
    profiles = SupplierProfile.objects.select_related("user").order_by("is_approved", "-created_at")
    return render(request, "suppliers/admin_approvals.html", {"profiles": profiles})


@login_required
@role_required("admin")
def admin_supplier_approve(request, pk):
    profile = get_object_or_404(SupplierProfile, pk=pk)
    profile.is_approved = True
    profile.approved_at = timezone.now()
    profile.save(update_fields=["is_approved", "approved_at"])
    messages.success(request, f"{profile} approved successfully.")
    return redirect("suppliers_admin:approvals")

