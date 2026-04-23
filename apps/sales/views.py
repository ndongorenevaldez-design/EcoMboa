from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.access import role_required
from apps.buyers.models import BuyerProfile

from .forms import SaleForm, SaleLineFormSet
from .models import Sale
from .services import calculate_sale_totals, generate_certificate_pdf, generate_invoice_pdf


@login_required
@role_required("buyer", "admin", "center")
def sale_list(request):
    sales = Sale.objects.select_related("buyer", "sorting_center", "created_by").prefetch_related("lines")
    if request.user.role == "buyer":
        buyer = get_object_or_404(BuyerProfile, user=request.user)
        sales = sales.filter(buyer=buyer)
    sales = sales.order_by("-created_at")
    return render(
        request,
        "sales/sale_list.html",
        {
            "sales": sales,
            "is_buyer_context": request.user.role == "buyer",
        },
    )


@login_required
@role_required("buyer", "admin", "center")
def sale_create(request):
    buyer_initial = None
    if request.user.role == "buyer":
        buyer_initial = get_object_or_404(BuyerProfile, user=request.user)

    if request.method == "POST":
        post_data = request.POST.copy()
        if buyer_initial:
            post_data["buyer"] = str(buyer_initial.pk)
        form = SaleForm(post_data)
        formset = SaleLineFormSet(request.POST, prefix="lines")
        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            if request.user.role == "buyer":
                sale.buyer = buyer_initial
                sale.status = "draft"
            sale.save()
            formset.instance = sale
            lines = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for line in lines:
                line.line_total = line.quantity_kg * line.unit_price
                line.save()
            calculate_sale_totals(sale)
            generate_invoice_pdf(sale)
            generate_certificate_pdf(sale)
            sale.save(update_fields=["invoice_pdf", "recycling_certificate_pdf", "updated_at"])
            messages.success(request, "Sale created successfully.")
            if request.user.role == "buyer":
                return redirect("buyer_sales:detail", pk=sale.pk)
            return redirect("sales:detail", pk=sale.pk)
        messages.error(request, "Please correct the highlighted fields.")
    else:
        initial = {"buyer": buyer_initial.pk} if buyer_initial else {}
        form = SaleForm(initial=initial)
        if request.user.role == "buyer":
            form.fields["buyer"].disabled = True
        formset = SaleLineFormSet(prefix="lines")
    return render(
        request,
        "sales/sale_form.html",
        {
            "form": form,
            "formset": formset,
            "is_buyer_context": request.user.role == "buyer",
        },
    )


@login_required
@role_required("buyer", "admin", "center")
def sale_detail(request, pk):
    sale = get_object_or_404(
        Sale.objects.select_related("buyer", "sorting_center", "created_by").prefetch_related("lines"),
        pk=pk,
    )
    if request.user.role == "buyer" and sale.buyer.user_id != request.user.id:
        return redirect("buyer_sales:index")
    return render(
        request,
        "sales/sale_detail.html",
        {"sale": sale, "is_buyer_context": request.user.role == "buyer"},
    )
