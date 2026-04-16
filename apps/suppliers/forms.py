from decimal import Decimal

from django import forms

from .models import SupplierProfile, SupplierTransaction


class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = [
            "business_name",
            "national_id_number",
            "preferred_mobile_money_operator",
            "preferred_mobile_money_number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class SupplierTransactionForm(forms.ModelForm):
    simulate_mobile_money = forms.BooleanField(
        required=False,
        initial=True,
        help_text="When enabled, payment is simulated and auto-marked paid.",
    )

    class Meta:
        model = SupplierTransaction
        fields = [
            "supplier",
            "material_type",
            "weight_kg",
            "price_per_kg",
            "mobile_money_operator",
            "mobile_money_number",
        ]
        widgets = {
            "weight_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
            "price_per_kg": forms.NumberInput(attrs={"step": "1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"].queryset = SupplierProfile.objects.filter(
            is_approved=True
        ).select_related("user").order_by("business_name", "user__username")
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

    def clean(self):
        data = super().clean()
        weight = data.get("weight_kg")
        price = data.get("price_per_kg")
        if weight is not None and price is not None:
            data["total_amount"] = (Decimal(weight) * Decimal(price)).quantize(
                Decimal("0.01")
            )
        return data

