from django import forms

from .models import CollectionPoint


class CollectionPointForm(forms.ModelForm):
    class Meta:
        model = CollectionPoint
        fields = [
            "name",
            "point_type",
            "status",
            "address",
            "district",
            "neighborhood",
            "latitude",
            "longitude",
            "manager",
            "accepts_plastic",
            "accepts_metal",
            "capacity_kg_day",
            "current_stock_kg",
            "fill_level",
            "plastic_price_kg",
            "metal_price_kg",
            "opening_time",
            "closing_time",
            "opening_days",
            "photo",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

