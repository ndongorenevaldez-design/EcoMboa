from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.access import role_required

from .forms import CSRReportForm, CollectionContractForm, PartnerProfileForm
from .models import CSRReport, CollectionContract, PartnerProfile
from .services import generate_csr_certificate


@login_required
@role_required("partner")
def partner_dashboard(request):
    profile = PartnerProfile.objects.filter(user=request.user).first()
    contracts = []
    reports = []
    if profile:
        contracts = profile.contracts.select_related("sorting_center").order_by("-created_at")
        reports = profile.csr_reports.order_by("-generated_at")
    return render(
        request,
        "partners/dashboard.html",
        {"profile": profile, "contracts": contracts, "reports": reports},
    )


@login_required
@role_required("partner")
def partner_profile_edit(request):
    profile = PartnerProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = PartnerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Partner profile saved.")
            return redirect("partners:index")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = PartnerProfileForm(instance=profile)
    return render(request, "partners/profile_form.html", {"form": form})


@login_required
@role_required("admin")
def admin_contract_list(request):
    contracts = CollectionContract.objects.select_related("partner", "sorting_center").order_by("-created_at")
    return render(request, "partners/contract_list.html", {"contracts": contracts})


@login_required
@role_required("admin")
def admin_contract_create(request):
    if request.method == "POST":
        form = CollectionContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Collection contract created.")
            return redirect("partners_admin:contracts")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = CollectionContractForm()
    return render(request, "partners/contract_form.html", {"form": form})


@login_required
@role_required("admin")
def admin_csr_report_create(request):
    if request.method == "POST":
        form = CSRReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            generate_csr_certificate(report)
            report.save()
            messages.success(request, "CSR report created.")
            return redirect("partners_admin:contracts")
        messages.error(request, "Please correct the highlighted fields.")
    else:
        form = CSRReportForm()
    return render(request, "partners/csr_form.html", {"form": form})

