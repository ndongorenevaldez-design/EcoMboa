from django import forms

from .models import CSRReport, CollectionContract, PartnerProfile


class PartnerProfileForm(forms.ModelForm):
    class Meta:
        model = PartnerProfile
        fields = ["company_name", "sector", "contact_person", "csr_objectives", "is_active"]
        widgets = {
            "csr_objectives": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class CollectionContractForm(forms.ModelForm):
    class Meta:
        model = CollectionContract
        fields = [
            "partner",
            "sorting_center",
            "start_date",
            "end_date",
            "target_collection_kg",
            "price_per_kg",
            "is_active",
            "terms",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "target_collection_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "price_per_kg": forms.NumberInput(attrs={"step": "1", "min": "0"}),
            "terms": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()


class CSRReportForm(forms.ModelForm):
    class Meta:
        model = CSRReport
        fields = [
            "partner",
            "reporting_period_start",
            "reporting_period_end",
            "total_collected_kg",
            "co2_avoided_kg",
            "impact_summary",
        ]
        widgets = {
            "reporting_period_start": forms.DateInput(attrs={"type": "date"}),
            "reporting_period_end": forms.DateInput(attrs={"type": "date"}),
            "total_collected_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "co2_avoided_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "impact_summary": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

