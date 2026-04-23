from django import forms

from .models import DeliveryReception, MaterialStock


class DeliveryReceptionForm(forms.ModelForm):
    class Meta:
        model = DeliveryReception
        fields = [
            "sorting_center",
            "mission",
            "supplier_transaction",
            "material_category",
            "quality_grade",
            "received_weight_kg",
            "lot_qr_code",
            "confirmation_photo",
            "notes",
        ]
        widgets = {
            "received_weight_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mission"].required = False
        self.fields["supplier_transaction"].required = False
        self.fields["lot_qr_code"].required = False
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

    def clean(self):
        data = super().clean()
        if not data.get("mission") and not data.get("supplier_transaction") and not data.get("lot_qr_code"):
            raise forms.ValidationError(
                "Provide a mission, a supplier transaction, or a lot QR code."
            )
        return data


class MaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = [
            "sorting_center",
            "material_category",
            "quality_grade",
            "quantity_kg",
            "low_stock_threshold_kg",
            "unit_price",
        ]
        widgets = {
            "quantity_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "low_stock_threshold_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "unit_price": forms.NumberInput(attrs={"step": "1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

