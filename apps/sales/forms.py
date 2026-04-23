from django import forms
from django.forms import inlineformset_factory

from .models import Sale, SaleLine


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["buyer", "sorting_center", "status", "due_date", "notes"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class SaleLineForm(forms.ModelForm):
    class Meta:
        model = SaleLine
        fields = ["material_category", "quality_grade", "quantity_kg", "unit_price"]
        widgets = {
            "quantity_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1"}),
            "unit_price": forms.NumberInput(attrs={"step": "1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


SaleLineFormSet = inlineformset_factory(
    Sale,
    SaleLine,
    form=SaleLineForm,
    extra=1,
    can_delete=True,
)

