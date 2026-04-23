from django import forms

from .models import BuyerProfile


class BuyerProfileForm(forms.ModelForm):
    desired_materials_text = forms.CharField(
        required=False,
        label="Desired materials",
        help_text="Comma-separated, for example: plastic, metal, paper",
    )

    class Meta:
        model = BuyerProfile
        fields = ["company_name", "trade_register_number", "monthly_capacity_kg"]
        widgets = {
            "monthly_capacity_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["desired_materials_text"].initial = ", ".join(self.instance.desired_materials or [])
        for field in self.fields.values():
            base = "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()

    def save(self, commit=True):
        profile = super().save(commit=False)
        materials = self.cleaned_data.get("desired_materials_text", "")
        profile.desired_materials = [item.strip() for item in materials.split(",") if item.strip()]
        if commit:
            profile.save()
        return profile

